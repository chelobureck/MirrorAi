from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.board import Board
from models.user import User
from schemas.board import BoardCreate, BoardResponse
from utils.auth import get_current_user
from sqlalchemy import select
import logging

# Настройка логирования для диагностики
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/boards", tags=["boards"])

@router.post("/", response_model=BoardResponse)
async def create_board(
    board: BoardCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Создание нового борда с улучшенной обработкой ошибок"""
    try:
        logger.info(f"Creating board for user {current_user.id}: {board.name}")
        
        new_board = Board(
            name=board.name, 
            description=board.description,
            user_id=current_user.id
        )
        session.add(new_board)
        await session.commit()
        await session.refresh(new_board)
        
        logger.info(f"Board created successfully: {new_board.id}")
        return new_board
        
    except Exception as e:
        logger.error(f"Error creating board: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания борда: {str(e)}"
        )

@router.get("/", response_model=List[BoardResponse])
async def get_boards(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Получение всех бордов пользователя с обработкой ошибок"""
    try:
        logger.info(f"Getting boards for user {current_user.id}")
        
        result = await session.execute(
            select(Board).where(Board.user_id == current_user.id)
        )
        boards = result.scalars().all()
        
        logger.info(f"Found {len(boards)} boards for user {current_user.id}")
        return boards
        
    except Exception as e:
        logger.error(f"Error getting boards: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения бордов: {str(e)}"
        )

@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Board).where(Board.id == board_id, Board.user_id == current_user.id))
    board = result.scalars().first()
    if not board:
        raise HTTPException(status_code=404, detail="Борд не найден")
    return board

@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Board).where(Board.id == board_id, Board.user_id == current_user.id))
    board = result.scalars().first()
    if not board:
        raise HTTPException(status_code=404, detail="Борд не найден")
    await session.delete(board)
    await session.commit()
    return {"ok": True}

@router.get("/test", tags=["debug"])
async def test_boards_endpoint():
    """Тестовый эндпоинт для проверки доступности роутера boards"""
    return {
        "status": "ok",
        "message": "Boards router is working",
        "timestamp": "2025-07-07T15:52:00Z",
        "available_endpoints": [
            "GET /api/v1/boards/ - Get user boards (auth required)",
            "POST /api/v1/boards/ - Create board (auth required)", 
            "GET /api/v1/boards/{id} - Get specific board (auth required)",
            "DELETE /api/v1/boards/{id} - Delete board (auth required)"
        ]
    }

@router.get("/health")
async def boards_health_check():
    """Простая проверка работоспособности boards роутера"""
    return {
        "status": "healthy",
        "service": "boards",
        "message": "Boards router is working",
        "endpoints": {
            "create": "POST /api/v1/boards/",
            "list": "GET /api/v1/boards/",
            "get": "GET /api/v1/boards/{id}",
            "delete": "DELETE /api/v1/boards/{id}"
        }
    }