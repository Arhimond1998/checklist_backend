from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.checklist_user_report import (
    ChecklistUserReportRepository,
)

from src.schemas import (
    ChecklistUserReportCreate,
    ChecklistUserReportTitle,
    ChecklistUserReportFull,
)
from src.deps.database import get_db
from src.deps.auth import get_current_user

router = APIRouter(prefix="/checklist_user_reports", tags=["Report"])


@router.post("/")
async def create_user_report(
    data: ChecklistUserReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ChecklistUserReportRepository(db)
    obj = await repo.create(data, current_user)
    await db.commit()
    return obj


@router.get("/titles", response_model=list[ChecklistUserReportTitle])
async def read_titles(db: AsyncSession = Depends(get_db)):
    repo = ChecklistUserReportRepository(db)

    return await repo.get_all_titles()


@router.get("/{id_checklist_user_report}", response_model=ChecklistUserReportFull)
async def read_checklist_user_report_full(
    id_checklist_user_report: int, db: AsyncSession = Depends(get_db)
):
    repo = ChecklistUserReportRepository(db)
    checklist = await repo.get_by_id_full(id_checklist_user_report)
    if not checklist:
        raise HTTPException(status_code=404, detail="checklist not found")
    return checklist
