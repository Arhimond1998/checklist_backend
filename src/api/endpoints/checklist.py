from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth import auth_service
from src.repositories.checklist import ChecklistRepository, get_repository
from src.repositories.file import FileRepository, get_file_repository
from src.repositories.user_checklist import UserChecklistRepository
from src.schemas import (
    Filters,
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
    UserChecklistCreate,
    ChecklistFullTitleResponse,
    ComboboxResponse,
)
from src.deps.database import get_db


router = APIRouter(prefix="/checklists", tags=["Checklist"])


@router.post("/", response_model=ChecklistResponse)
@auth_service.check_components(["constructor"])
async def create_checklist(
    request: Request,
    checklist: ChecklistCreate,
    repo: ChecklistRepository = Depends(get_repository),
    db: AsyncSession = Depends(get_db),
):
    new_checklist = await repo.create(checklist)
    user_checklist_repo = UserChecklistRepository(db)
    await user_checklist_repo.create(
        UserChecklistCreate(
            id_user=repo.user.id_user, id_checklist=new_checklist.id_checklist
        )
    )

    await db.commit()
    return new_checklist


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(
    request: Request,
    repo: ChecklistRepository = Depends(get_repository),
):
    return await repo.get_combo()


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
    repo: ChecklistRepository = Depends(get_repository),
):
    checklists = await repo.get_all()
    return checklists


@router.post("/titles", response_model=list[ChecklistFullTitleResponse])
async def read_checklists_titles(
    filters: Filters,
    repo: ChecklistRepository = Depends(get_repository),
):
    checklists = await repo.get_all_titles_expanded(filters)
    return [
        ChecklistFullTitleResponse(**r.model_dump(exclude=["data"])) for r in checklists
    ]


@router.get("/{id_checklist}", response_model=ChecklistResponse)
async def read_checklist(
    id_checklist: int,
    repo: ChecklistRepository = Depends(get_repository),
):
    checklist = await repo.get_by_id_info(id_checklist)
    if not checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return checklist


@router.put("/{id_checklist}", response_model=ChecklistResponse)
@auth_service.check_components(["constructor"])
async def update_checklist(
    request: Request,
    id_checklist: int,
    checklist: ChecklistUpdate,
    repo: ChecklistRepository = Depends(get_repository),
    db: AsyncSession = Depends(get_db),
):
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
    repo: ChecklistRepository = Depends(get_repository),
    db: AsyncSession = Depends(get_db),
):
    success = await repo.delete(id_checklist)
    if not success:
        raise HTTPException(status_code=404, detail="checklist not found")
    await db.commit()
    return {"message": "checklist deleted"}
