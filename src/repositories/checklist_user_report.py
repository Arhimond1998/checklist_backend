from sqlalchemy import select, func
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
    Filters,
)
from src.repositories.base import RepositoryBase


class ChecklistUserReportRepository(
    RepositoryBase[
        ChecklistUserReport, ChecklistUserReportCreate, ChecklistUserReportUpdate
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(ChecklistUserReport, db)

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

    async def get_all_titles(self, filters: Filters) -> list[ChecklistUserReportTitle]:
        stmt = (
            select(
                ChecklistUserReport.id_checklist_user_report,
                ChecklistUserReport.id_checklist,
                ChecklistUserReport.id_user,
                ChecklistUserReport.id_employee,
                ChecklistUserReport.commentary,
                ChecklistUserReport.score,
                ChecklistUserReport.max_score,
                ChecklistUserReport.dt,
                User.surname.label("user_surname"),
                User.name.label("user_name"),
                User.patronymic.label("user_patronymic"),
                Employee.surname.label("employee_surname"),
                Employee.name.label("employee_name"),
                Employee.patronymic.label("employee_patronymic"),
                Checklist.title,
                Store.name.label("name_store"),
                Store.code.label("code_store"),
                Store.id_store,
            )
            .select_from(ChecklistUserReport)
            .join(User, User.id_user == ChecklistUserReport.id_user)
            .join(Checklist, Checklist.id_checklist == ChecklistUserReport.id_checklist)
            .join(
                StoreChecklist,
                StoreChecklist.id_checklist == ChecklistUserReport.id_checklist,
            )
            .join(Store, Store.id_store == StoreChecklist.id_store)
            .outerjoin(
                Employee, Employee.id_employee == ChecklistUserReport.id_employee
            )
        )
        stmt = self.apply_filters(stmt, filters)
        result = (await self.db.execute(stmt)).fetchall()
        return [
            ChecklistUserReportTitle(
                id_checklist_user_report=r.id_checklist_user_report,
                id_checklist=r.id_checklist,
                id_employee=r.id_employee,
                id_user=r.id_user,
                commentary=r.commentary,
                score=r.score,
                max_score=r.max_score,
                dt=r.dt,
                title=r.title,
                user_fullname=(r.user_surname or "").strip()
                + (r.user_name or "").strip()
                + (r.user_patronymic or "").strip(),
                employee_fullname=(r.employee_surname or "").strip()
                + (r.employee_name or "").strip()
                + (r.employee_patronymic or "").strip(),
                name_store=r.name_store,
                code_store=r.code_store,
                id_store=r.id_store,
            )
            for r in result
        ]

    async def get_by_id_full(
        self, id_checklist_user_report: int
    ) -> ChecklistUserReportFull | None:
        result = await self.db.execute(
            select(
                ChecklistUserReport.id_checklist_user_report,
                ChecklistUserReport.id_checklist,
                ChecklistUserReport.id_user,
                ChecklistUserReport.commentary,
                ChecklistUserReport.score,
                ChecklistUserReport.max_score,
                ChecklistUserReport.dt,
                ChecklistUserReport.data,
                Store.id_store,
                User.surname.concat(" ")
                .concat(User.name)
                .concat(" ")
                .concat(User.patronymic)
                .label("user_fullname"),
                Checklist.title,
                Store.name.label("name_store"),
                Store.code.label("code_store"),
                Employee.surname.concat(" ")
                .concat(User.name)
                .concat(" ")
                .concat(User.patronymic)
                .label("employee_fullname"),
            )
            .select_from(ChecklistUserReport)
            .join(User, User.id_user == ChecklistUserReport.id_user)
            .join(Checklist, Checklist.id_checklist == ChecklistUserReport.id_checklist)
            .join(StoreChecklist, StoreChecklist.id_checklist == Checklist.id_checklist)
            .join(Store, Store.id_store == StoreChecklist.id_store)
            .outerjoin(
                Employee, Employee.id_employee == ChecklistUserReport.id_employee
            )
            .where(
                ChecklistUserReport.id_checklist_user_report == id_checklist_user_report
            )
        )
        record = result.fetchone()
        return ChecklistUserReportFull(
            id_checklist_user_report=record.id_checklist_user_report,
            id_checklist=record.id_checklist,
            id_user=record.id_user,
            commentary=record.commentary,
            id_store=record.id_store,
            name_store=record.name_store,
            code_store=record.code_store,
            score=record.score,
            max_score=record.max_score,
            dt=record.dt,
            title=record.title,
            user_fullname=record.user_fullname,
            employee_fullname=record.employee_fullname,
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


def get_repository(db: AsyncSession) -> ChecklistUserReportRepository:
    return ChecklistUserReportRepository(db)
