from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth import auth_service
from src.repositories.checklist import ChecklistRepository
from src.repositories.file import FileRepository, get_file_repository
from src.repositories.user_checklist import UserChecklistRepository
from src.schemas import (
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
    UserChecklistCreate,
    ChecklistTitlesResponse,
    ComboboxResponse,
)
from src.models.user import User
from src.deps.database import get_db
from src.deps.auth import get_current_user

router = APIRouter(prefix="/checklists", tags=["Checklist"])


@router.post("/", response_model=ChecklistResponse)
@auth_service.check_components(["constructor"])
async def create_checklist(
    request: Request,
    checklist: ChecklistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ChecklistRepository(db, current_user)
    new_checklist = await repo.create(checklist)
    user_checklist_repo = UserChecklistRepository(db)
    await user_checklist_repo.create(
        UserChecklistCreate(
            id_user=current_user.id_user, id_checklist=new_checklist.id_checklist
        )
    )

    await db.commit()
    return new_checklist


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    role_repo = ChecklistRepository(db, current_user)
    return await role_repo.get_combo()


@router.post("/upload")
@auth_service.check_components(["constructor"])
async def upload_photo(
    request: Request,
    files: list[UploadFile],
    file_repo: FileRepository = Depends(get_file_repository),
):
    return await file_repo.create_bunch(files)


@router.get("/", response_model=list[ChecklistResponse])
async def read_checklists(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db, current_user)
    checklists = await repo.get_all()
    return checklists


@router.get("/titles", response_model=list[ChecklistTitlesResponse])
async def read_checklists_titles(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = ChecklistRepository(db, current_user)
    checklists = await repo.get_all()
    return checklists


@router.get("/{id_checklist}", response_model=ChecklistResponse)
async def read_checklist(
    id_checklist: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ChecklistRepository(db, current_user)
    checklist = await repo.get_by_id(id_checklist)
    if not checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return checklist


@router.put("/{id_checklist}", response_model=ChecklistResponse)
@auth_service.check_components(["constructor"])
async def update_checklist(
    request: Request,
    id_checklist: int,
    checklist: ChecklistUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ChecklistRepository(db, current_user)
    updated_checklist = await repo.update(id_checklist, checklist)
    if not updated_checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    await db.commit()
    return updated_checklist


@router.delete("/{id_checklist}")
@auth_service.check_components(["constructor"])
async def delete_checklist(
    request: Request,
    id_checklist: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ChecklistRepository(db, current_user)
    success = await repo.delete(id_checklist)
    if not success:
        raise HTTPException(status_code=404, detail="checklist not found")
    await db.commit()
    return {"message": "checklist deleted"}
