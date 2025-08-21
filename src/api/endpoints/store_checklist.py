from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.store_checklist import StoreChecklistRepository
from src.schemas import (
    StoreChecklistCreate,
    StoreChecklistResponse,
    StoreChecklistFullResponse,
)
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/store_checklists", tags=["StoreChecklist"])


@router.post("/", response_model=StoreChecklistResponse)
@auth_service.check_roles(["admin"])
async def create_store_checklist(
    request: Request,
    store_checklist: StoreChecklistCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = StoreChecklistRepository(db)
    obj = await repo.create(store_checklist)
    await db.commit()
    return obj


@router.get("/", response_model=list[StoreChecklistResponse])
async def read_store_checklists(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreChecklistRepository(db)
    return await repo.get_all()


@router.get("/{store_checklist_id}", response_model=StoreChecklistResponse)
async def read_store_checklist(
    request: Request, store_checklist_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreChecklistRepository(db)
    store_checklist = await repo.get_by_id(store_checklist_id)
    if not store_checklist:
        raise HTTPException(status_code=404, detail="store_checklist not found")
    return store_checklist


@router.post("/get_full", response_model=list[StoreChecklistFullResponse])
async def get_full(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreChecklistRepository(db)
    return await repo.get_all_full()


@router.delete("/{store_checklist_id}")
@auth_service.check_roles(["admin"])
async def delete_store_checklist(
    request: Request, store_checklist_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreChecklistRepository(db)
    success = await repo.delete(store_checklist_id)
    if not success:
        raise HTTPException(status_code=404, detail="store_checklist not found")
    await db.commit()
    return {"message": "store_checklist deleted"}
