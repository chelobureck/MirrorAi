from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from models.base import get_session
from models.user import User
from schemas.user import UserCreate, UserResponse, Token, EmailVerificationRequest, EmailVerificationResponse
from utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    get_current_user_by_refresh_token
)
from config.settings import get_settings
from fastapi.responses import RedirectResponse
import httpx
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # Проверяем, существует ли пользователь
    result = await session.execute(
        select(User).where((User.email == user_data.email) | (User.username == user_data.username))
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email или имя пользователя уже зарегистрированы"
        )
    # Мок-подтверждение email (реально email не отправляем)
    is_email_verified = True
    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        role="user",
        credits=0
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    # Проверяем существование пользователя
    result = await session.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "credits": user.credits}, expires_delta=access_token_expires
    )
    # Генерация refresh токена (на 7 дней)
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(
        data={"sub": user.email, "type": "refresh"}, expires_delta=refresh_token_expires
    )
    # refresh_token можно возвращать в httpOnly cookie (реализовать на фронте)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str = Cookie(None),
    session: AsyncSession = Depends(get_session)
):
    user = await get_current_user_by_refresh_token(refresh_token, session)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "credits": user.credits}, expires_delta=access_token_expires
    )
    # refresh_token не обновляем, возвращаем тот же
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/google-login")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        "scope=openid%20email%20profile&"
        "access_type=offline"
    )
    return RedirectResponse(google_auth_url)

@router.get("/google-callback")
async def google_callback(code: str, session: AsyncSession = Depends(get_session)):
    # Получаем токен Google
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_resp.json()
        id_token = token_data.get("id_token")
        access_token = token_data.get("access_token")
    # Получаем профиль пользователя
    async with httpx.AsyncClient() as client:
        userinfo_resp = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        userinfo = userinfo_resp.json()
    email = userinfo.get("email")
    username = userinfo.get("name") or email.split("@")[0]
    # Проверяем, есть ли пользователь
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalars().first()
    if not user:
        user = User(
            email=email,
            username=username,
            hashed_password="google_oauth",
            role="user",
            credits=0
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    # Генерируем токены
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "credits": user.credits}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_access_token(
        data={"sub": user.email, "type": "refresh"}, expires_delta=refresh_token_expires
    )
    # Можно сделать редирект на фронт с токенами в query params или cookie
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/email-verification-request", response_model=EmailVerificationResponse)
async def email_verification_request(
    data: EmailVerificationRequest,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    token = secrets.token_urlsafe(32)
    user.email_verification_token = token
    await session.commit()
    # Здесь должна быть отправка email (заглушка)
    return EmailVerificationResponse(message="Письмо отправлено (заглушка)")

@router.get("/verify-email", response_model=EmailVerificationResponse)
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.email_verification_token == token)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Неверный токен")
    user.is_email_verified = True
    user.email_verification_token = None
    await session.commit()
    return EmailVerificationResponse(message="Email подтверждён")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user 