from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models.base import get_session
from models.board import Board
from models.user import User
from schemas.board import BoardCreate, BoardResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/boards", tags=["boards"])

@router.post("/", response_model=BoardResponse)
async def create_board(
    board: BoardCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    new_board = Board(name=board.name, user_id=current_user.id)
    session.add(new_board)
    await session.commit()
    await session.refresh(new_board)
    return new_board

@router.get("/", response_model=List[BoardResponse])
async def get_boards(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    boards = await session.query(Board).filter(Board.user_id == current_user.id).all()
    return boards

@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    board = await session.query(Board).filter(Board.id == board_id, Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Борд не найден")
    return board

@router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    board = await session.query(Board).filter(Board.id == board_id, Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Борд не найден")
    await session.delete(board)
    await session.commit()
    return {"ok": True} 