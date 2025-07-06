"""
Guest Credits Service - управление кредитами гостей
"""
import uuid
import json
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
import redis.asyncio as redis
from models.guest_session import GuestSession
from config.settings import get_settings

settings = get_settings()

class GuestCreditsService:
    """Сервис для управления кредитами гостей"""
    
    def __init__(self):
        self.redis_client = None
        self.redis_ttl = 86400 * 7  # 7 дней
    
    async def get_redis_client(self):
        """Получение Redis клиента"""
        if not self.redis_client:
            self.redis_client = redis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def get_or_create_guest_session(
        self, 
        session_id: Optional[str], 
        ip_address: str, 
        user_agent: str,
        db: AsyncSession
    ) -> tuple[str, int]:
        """
        Получить или создать сессию гостя
        Возвращает: (session_id, credits)
        """
        # Если session_id не передан, создаем новый
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Проверяем в Redis
        redis_client = await self.get_redis_client()
        redis_key = f"guest_credits:{session_id}"
        
        try:
            redis_data = await redis_client.get(redis_key)
            if redis_data:
                guest_data = json.loads(redis_data)
                # Обновляем последнее использование в БД
                await self._update_last_used(session_id, db)
                return session_id, guest_data["credits"]
        except Exception as e:
            print(f"Redis error: {e}")
        
        # Проверяем в БД
        stmt = select(GuestSession).where(GuestSession.session_id == session_id)
        result = await db.execute(stmt)
        guest_session = result.scalars().first()
        
        if guest_session:
            # Синхронизируем с Redis
            await self._sync_to_redis(guest_session)
            return session_id, guest_session.credits
        
        # Создаем новую сессию
        new_session = GuestSession(
            session_id=session_id,
            credits=50,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        
        # Сохраняем в Redis
        await self._sync_to_redis(new_session)
        
        return session_id, 50
    
    async def use_credit(self, session_id: str, db: AsyncSession) -> bool:
        """
        Списать один кредит
        Возвращает True если кредит списан успешно, False если недостаточно кредитов
        """
        redis_client = await self.get_redis_client()
        redis_key = f"guest_credits:{session_id}"
        
        try:
            # Пытаемся списать из Redis
            redis_data = await redis_client.get(redis_key)
            if redis_data:
                guest_data = json.loads(redis_data)
                if guest_data["credits"] > 0:
                    guest_data["credits"] -= 1
                    guest_data["last_used"] = datetime.now().isoformat()
                    await redis_client.set(redis_key, json.dumps(guest_data), ex=self.redis_ttl)
                    
                    # Асинхронно обновляем БД
                    await self._update_credits_in_db(session_id, guest_data["credits"], db)
                    return True
                return False
        except Exception as e:
            print(f"Redis error during credit usage: {e}")
        
        # Fallback к БД
        stmt = select(GuestSession).where(GuestSession.session_id == session_id)
        result = await db.execute(stmt)
        guest_session = result.scalars().first()
        
        if not guest_session or guest_session.credits <= 0:
            return False
        
        # Обновляем в БД
        stmt = update(GuestSession).where(
            GuestSession.session_id == session_id
        ).values(
            credits=GuestSession.credits - 1,
            last_used_at=func.now()
        )
        await db.execute(stmt)
        await db.commit()
        
        # Синхронизируем с Redis
        guest_session.credits -= 1
        await self._sync_to_redis(guest_session)
        
        return True
    
    async def get_credits(self, session_id: str, db: AsyncSession) -> int:
        """Получить количество кредитов"""
        redis_client = await self.get_redis_client()
        redis_key = f"guest_credits:{session_id}"
        
        try:
            redis_data = await redis_client.get(redis_key)
            if redis_data:
                guest_data = json.loads(redis_data)
                return guest_data["credits"]
        except Exception as e:
            print(f"Redis error: {e}")
        
        # Fallback к БД
        stmt = select(GuestSession).where(GuestSession.session_id == session_id)
        result = await db.execute(stmt)
        guest_session = result.scalars().first()
        
        return guest_session.credits if guest_session else 0
    
    async def refund_credit(self, session_id: str, db: AsyncSession) -> bool:
        """
        Возврат кредита в случае ошибки генерации
        Возвращает True если кредит возвращен успешно
        """
        redis_client = await self.get_redis_client()
        redis_key = f"guest_credits:{session_id}"
        
        try:
            # Пытаемся вернуть кредит в Redis
            redis_data = await redis_client.get(redis_key)
            if redis_data:
                guest_data = json.loads(redis_data)
                guest_data["credits"] += 1
                guest_data["last_used"] = datetime.now().isoformat()
                await redis_client.set(redis_key, json.dumps(guest_data), ex=self.redis_ttl)
                
                # Асинхронно обновляем БД
                await self._update_credits_in_db(session_id, guest_data["credits"], db)
                return True
        except Exception as e:
            print(f"Redis error during credit refund: {e}")
        
        # Fallback к БД
        stmt = select(GuestSession).where(GuestSession.session_id == session_id)
        result = await db.execute(stmt)
        guest_session = result.scalars().first()
        
        if not guest_session:
            return False
        
        # Обновляем в БД
        stmt = update(GuestSession).where(
            GuestSession.session_id == session_id
        ).values(
            credits=GuestSession.credits + 1,
            last_used_at=func.now()
        )
        await db.execute(stmt)
        await db.commit()
        
        # Синхронизируем с Redis
        guest_session.credits += 1
        await self._sync_to_redis(guest_session)
        
        return True

    async def _sync_to_redis(self, guest_session: GuestSession):
        """Синхронизация данных сессии в Redis"""
        try:
            redis_client = await self.get_redis_client()
            redis_key = f"guest_credits:{guest_session.session_id}"
            guest_data = {
                "credits": guest_session.credits,
                "created_at": guest_session.created_at.isoformat(),
                "last_used": guest_session.last_used_at.isoformat()
            }
            await redis_client.set(redis_key, json.dumps(guest_data), ex=self.redis_ttl)
        except Exception as e:
            print(f"Redis sync error: {e}")
    
    async def _update_last_used(self, session_id: str, db: AsyncSession):
        """Обновить время последнего использования"""
        stmt = update(GuestSession).where(
            GuestSession.session_id == session_id
        ).values(last_used_at=func.now())
        await db.execute(stmt)
        await db.commit()
    
    async def _update_credits_in_db(self, session_id: str, credits: int, db: AsyncSession):
        """Обновить кредиты в БД"""
        stmt = update(GuestSession).where(
            GuestSession.session_id == session_id
        ).values(
            credits=credits,
            last_used_at=func.now()
        )
        await db.execute(stmt)
        await db.commit()

# Синглтон сервиса
guest_credits_service = GuestCreditsService()
