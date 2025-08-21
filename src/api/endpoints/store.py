from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.store import StoreRepository
from src.schemas import StoreCreate, StoreUpdate, StoreResponse, ComboboxResponse
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/stores", tags=["Store"])


@router.post("/", response_model=StoreResponse)
@auth_service.check_roles(["admin"])
async def create_store(
    request: Request, store: StoreCreate, db: AsyncSession = Depends(get_db)
):
    repo = StoreRepository(db)
    obj = await repo.create(store)
    await db.commit()
    return obj


@router.get("/", response_model=list[StoreResponse])
async def read_stores(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreRepository(db)
    return await repo.get_all()


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(request: Request, db: AsyncSession = Depends(get_db)):
    store_repo = StoreRepository(db)
    return await store_repo.get_combo()


@router.get("/{store_id}", response_model=StoreResponse)
async def read_store(
    request: Request, store_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreRepository(db)
    store = await repo.get_by_id(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="store not found")
    await db.commit()
    return store


@router.put("/{store_id}", response_model=StoreResponse)
@auth_service.check_roles(["admin"])
async def update_store(
    request: Request,
    store_id: int,
    store: StoreUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = StoreRepository(db)
    updated_store = await repo.update(store_id, store)
    if not updated_store:
        raise HTTPException(status_code=404, detail="store not found")
    return updated_store


@router.delete("/{store_id}")
@auth_service.check_roles(["admin"])
async def delete_store(
    request: Request, store_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreRepository(db)
    success = await repo.delete(store_id)
    if not success:
        raise HTTPException(status_code=404, detail="store not found")
    await db.commit()
    return {"message": "store deleted"}
