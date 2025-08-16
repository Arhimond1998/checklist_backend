from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.checklist import ChecklistRepository
from src.repositories.file import FileRepository, get_file_repository
from src.repositories.user_checklist import UserChecklistRepository
from src.schemas import (
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
    UserChecklistCreate,
    ChecklistTitlesResponse,
    ChecklistUserReportCreate,
)
from src.deps.database import get_db
from src.deps.auth import get_current_user

router = APIRouter(prefix="/checklists")


@router.post("/", response_model=ChecklistResponse)
async def create_checklist(
    checklist: ChecklistCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ChecklistRepository(db)
    new_checklist = await repo.create(checklist)
    user_checklist_repo = UserChecklistRepository(db)
    await user_checklist_repo.create(
        UserChecklistCreate(
            id_user=current_user.id_user, id_checklist=new_checklist.id_checklist
        )
    )

    await db.commit()
    return new_checklist


@router.post("/save_user_report")
async def create_user_report(
    data: ChecklistUserReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ChecklistRepository(db)
    return await repo.create_user_report(data, current_user)


@router.post("/upload")
async def upload_photo(
    files: list[UploadFile], file_repo: FileRepository = Depends(get_file_repository)
):
    return await file_repo.create_bunch(files)


@router.get("/", response_model=list[ChecklistResponse])
async def read_checklists(db: AsyncSession = Depends(get_db)):
    repo = ChecklistRepository(db)
    checklists = await repo.get_all()
    return checklists


@router.get("/titles", response_model=list[ChecklistTitlesResponse])
async def read_checklists_titles(db: AsyncSession = Depends(get_db)):
    repo = ChecklistRepository(db)
    checklists = await repo.get_all()
    return checklists


@router.get("/{id_checklist}", response_model=ChecklistResponse)
async def read_checklist(id_checklist: int, db: AsyncSession = Depends(get_db)):
    repo = ChecklistRepository(db)
    checklist = await repo.get_by_id(id_checklist)
    if not checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return checklist


@router.put("/{id_checklist}", response_model=ChecklistResponse)
async def update_checklist(
    id_checklist: int, checklist: ChecklistUpdate, db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db)
    updated_checklist = await repo.update(id_checklist, checklist)
    if not updated_checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    await db.commit()
    return updated_checklist


@router.delete("/{id_checklist}")
async def delete_checklist(id_checklist: int, db: AsyncSession = Depends(get_db)):
    repo = ChecklistRepository(db)
    success = await repo.delete(id_checklist)
    if not success:
        raise HTTPException(status_code=404, detail="checklist not found")
    await db.commit()
    return {"message": "checklist deleted"}
