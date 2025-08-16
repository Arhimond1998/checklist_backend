from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import ChecklistUserReport
from src.models import User
from src.schemas import ChecklistUserReportCreate, ChecklistUserReportUpdate


class ChecklistUserReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, create_data: ChecklistUserReportCreate, user: User
    ) -> ChecklistUserReport:
        new_obj = ChecklistUserReport(
            **(create_data.model_dump() | {"id_user": user.id_user})
        )
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(
        self, id_checklist_user_report: int
    ) -> ChecklistUserReport | None:
        result = await self.db.execute(
            select(ChecklistUserReport).filter(
                ChecklistUserReport.id_checklist_user_report == id_checklist_user_report
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ChecklistUserReport]:
        result = await self.db.execute(select(ChecklistUserReport))
        return result.scalars().all()

    async def update(
        self,
        id_checklist_user_report: int,
        update_data: ChecklistUserReportUpdate,
    ) -> ChecklistUserReport | None:
        db_obj = await self.get_by_id(id_checklist_user_report)
        for k, v in update_data.model_dump().items():
            setattr(db_obj, k, v)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id_checklist_user_report: int) -> bool:
        db_obj = await self.get_by_id(id_checklist_user_report)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
