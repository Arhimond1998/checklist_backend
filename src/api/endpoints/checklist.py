from fastapi import APIRouter, Depends, HTTPException
from src.repositories.checklist import ChecklistRepository
from src.schemas import ChecklistCreate, ChecklistResponse, ChecklistUpdate
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/checklists')

@router.post("/", response_model=ChecklistResponse)
async def create_checklist(
    checklist: ChecklistCreate, 
    db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    return await repo.create(checklist)

@router.get("/", response_model=list[ChecklistResponse])
async def read_checklists(
    db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    return await repo.get_all()

@router.get("/{id_checklist}", response_model=ChecklistResponse)
async def read_checklist(
    id_checklist: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    checklist = await repo.get_by_id(id_checklist)
    if not checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return checklist

@router.put("/{id_checklist}", response_model=ChecklistResponse)
async def update_checklist(
    id_checklist: int, 
    checklist: ChecklistUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    updated_checklist = await repo.update(id_checklist, checklist)
    if not updated_checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return updated_checklist

@router.delete("/{id_checklist}")
async def delete_checklist(
    id_checklist: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    success = await repo.delete(id_checklist)
    if not success:
        raise HTTPException(status_code=404, detail="checklist not found")
    return {"message": "checklist deleted"}