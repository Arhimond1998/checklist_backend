from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.checklist_user_report import (
    ChecklistUserReportUserReportRepository,
)

from src.schemas import (
    ChecklistUserReportCreate,
)
from src.deps.database import get_db
from src.deps.auth import get_current_user

router = APIRouter(prefix="/checklist_user_report")


@router.post("/")
async def create_user_report(
    data: ChecklistUserReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = ChecklistUserReportUserReportRepository(db)
    return await repo.create(data, current_user)
