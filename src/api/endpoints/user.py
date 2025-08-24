from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.schemas import UserCreate, UserUpdate, UserResponse, ComboboxResponse, ComboboxTreeResponse
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
@auth_service.check_roles(["admin"])
async def create_user(
    request: Request, user: UserCreate, db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user.password = auth_service.hash_password(user.password)
    new_user = await user_repo.create(user)
    await db.commit()
    return new_user


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(request: Request, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    return await user_repo.get_combo()


@router.get("/", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
@auth_service.check_roles(["admin"])
async def update_user(
    request: Request, user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    updated_user = await repo.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="user not found")
    await db.commit()
    return updated_user


@router.delete("/{user_id}")
@auth_service.check_roles(["admin"])
async def delete_user(
    request: Request, user_id: int, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="user not found")
    await db.commit()
    return {"message": "user deleted"}
