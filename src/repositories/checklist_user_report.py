from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import ChecklistUserReport
from src.models import User
from src.models import Checklist
from src.models import Employee
from src.models import StoreChecklist
from src.models import Store
from src.schemas import (
    ChecklistUserReportCreate,
    ChecklistUserReportUpdate,
    ChecklistUserReportTitle,
    ChecklistUserReportFull,
)


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

    async def get_all_titles(self) -> list[ChecklistUserReportTitle]:
        result = await self.db.execute(
            select(
                ChecklistUserReport.id_checklist_user_report,
                ChecklistUserReport.id_checklist,
                ChecklistUserReport.id_user,
                ChecklistUserReport.id_employee,
                ChecklistUserReport.score,
                ChecklistUserReport.max_score,
                ChecklistUserReport.dt,
                User.surname.concat(" ")
                .concat(User.name)
                .concat(" ")
                .concat(User.patronymic)
                .label("user_fullname"),
                Employee.surname.concat(" ")
                .concat(Employee.name)
                .concat(" ")
                .concat(Employee.patronymic)
                .label("employee_fullname"),
                Checklist.title,
                Store.name.label('name_store'),
                Store.code.label('code_store'),
            )
            .join(User, User.id_user == ChecklistUserReport.id_user)
            .join(Checklist, Checklist.id_checklist == ChecklistUserReport.id_checklist)
            .join(StoreChecklist, StoreChecklist.id_checklist == ChecklistUserReport.id_checklist)
            .join(Store, Store.id_store == StoreChecklist.id_store)
            .outerjoin(Employee, Employee.id_employee == ChecklistUserReport.id_employee)
        )
        return [
            ChecklistUserReportTitle(
                id_checklist_user_report=r.id_checklist_user_report,
                id_checklist=r.id_checklist,
                id_employee=r.id_employee,
                id_user=r.id_user,
                score=r.score,
                max_score=r.max_score,
                dt=r.dt,
                title=r.title,
                user_fullname=r.user_fullname,
                employee_fullname=r.employee_fullname,
                name_store=r.name_store,
                code_store=r.code_store,
            )
            for r in result.fetchall()
        ]

    async def get_by_id_full(
        self, id_checklist_user_report: int
    ) -> ChecklistUserReportFull | None:
        result = await self.db.execute(
            select(
                ChecklistUserReport.id_checklist_user_report,
                ChecklistUserReport.id_checklist,
                ChecklistUserReport.id_user,
                ChecklistUserReport.score,
                ChecklistUserReport.max_score,
                ChecklistUserReport.dt,
                ChecklistUserReport.data,
                User.surname.concat(" ")
                .concat(User.name)
                .concat(" ")
                .concat(User.patronymic)
                .label("user_fullname"),
                Checklist.title,
            )
            .join(User, User.id_user == ChecklistUserReport.id_user)
            .join(Checklist, Checklist.id_checklist == ChecklistUserReport.id_checklist)
            .where(
                ChecklistUserReport.id_checklist_user_report == id_checklist_user_report
            )
        )
        record = result.fetchone()
        return ChecklistUserReportFull(
            id_checklist_user_report=record.id_checklist_user_report,
            id_checklist=record.id_checklist,
            id_user=record.id_user,
            score=record.score,
            max_score=record.max_score,
            dt=record.dt,
            title=record.title,
            user_fullname=record.user_fullname,
            data=record.data,
        )

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
