from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_role import UserRoleRepository
from src.schemas import UserRoleCreate, UserRoleResponse, UserRoleFullResponse
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/user_roles", tags=["User role"])


@router.post("/", response_model=UserRoleResponse)
@auth_service.check_roles(["admin"])
async def create_user(
    request: Request, user: UserRoleCreate, db: AsyncSession = Depends(get_db)
):
    repo = UserRoleRepository(db)
    obj = await repo.create(user)
    await db.commit()
    return obj


@router.get("/", response_model=list[UserRoleFullResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    repo = UserRoleRepository(db)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserRoleFullResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRoleRepository(db)
    user_role = await repo.get_by_id(user_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="user role not found")
    return user_role


@router.delete("/{user_id}")
@auth_service.check_roles(["admin"])
async def delete_user(
    request: Request, user_id: int, db: AsyncSession = Depends(get_db)
):
    repo = UserRoleRepository(db)
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="user role not found")
    await db.commit()
    return {"message": "user role deleted"}
