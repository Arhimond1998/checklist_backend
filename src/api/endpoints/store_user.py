from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.store_user import StoreUserRepository
from src.schemas import StoreUserCreate, StoreUserResponse, StoreUserFullResponse
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/store_users", tags=["StoreUser"])


@router.post("/", response_model=StoreUserResponse)
@auth_service.check_roles(["admin"])
async def create_store_user(
    request: Request, store_user: StoreUserCreate, db: AsyncSession = Depends(get_db)
):
    repo = StoreUserRepository(db)
    obj = await repo.create(store_user)
    await db.commit()
    return obj


@router.post("/get_full", response_model=list[StoreUserFullResponse])
async def get_full(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreUserRepository(db)
    return await repo.get_all_full()


@router.get("/", response_model=list[StoreUserResponse])
async def read_store_users(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreUserRepository(db)
    return await repo.get_all()


@router.get("/{store_user_id}", response_model=StoreUserResponse)
async def read_store_user(
    request: Request, store_user_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreUserRepository(db)
    store_user = await repo.get_by_id(store_user_id)
    if not store_user:
        raise HTTPException(status_code=404, detail="store_user not found")
    return store_user


@router.delete("/{store_user_id}")
@auth_service.check_roles(["admin"])
async def delete_store_user(
    request: Request, store_user_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreUserRepository(db)
    success = await repo.delete(store_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="store_user not found")
    await db.commit()
    return {"message": "store_user deleted"}
