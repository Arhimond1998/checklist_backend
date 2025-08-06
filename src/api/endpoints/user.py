from fastapi import APIRouter, Depends, HTTPException
from src.repositories.user import UserRepository
from src.schemas import UserCreate, UserUpdate, UserResponse
from src.deps.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/users')

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    return await repo.create(user)

@router.get("/", response_model=list[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    return await repo.get_all()

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    updated_user = await repo.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="user not found")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="user not found")
    return {"message": "user deleted"}