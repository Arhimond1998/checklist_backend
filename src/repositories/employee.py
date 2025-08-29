from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Employee, StoreEmployee
from src.schemas import EmployeeCreate, EmployeeUpdate, ComboboxResponse, Filters
from src.repositories.base import RepositoryBase


class EmployeeRepository(RepositoryBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Employee, db)

    async def create(self, create_dto: EmployeeCreate) -> Employee:
        return await super().create(create_dto)

    async def get_by_id(self, id_entity: int) -> Employee | None:
        return await self.get(Employee.id_employee == id_entity)

    async def get_all(self, filters: Filters) -> list[Employee]:
        stmt = self.apply_filters(select(Employee), filters)
        return (await self.db.execute(stmt)).fetchall()

    async def get_combo(self, filters: Filters) -> list[ComboboxResponse[int]]:
        stmt = self.apply_filters(
            select(
                Employee.surname,
                Employee.name,
                Employee.patronymic,
                Employee.id_employee,
                StoreEmployee.id_store,
            ).outerjoin(
                StoreEmployee, StoreEmployee.id_employee == Employee.id_employee
            ),
            filters,
        )
        result = []
        for record in (await self.db.execute(stmt)).fetchall():
            result.append(
                ComboboxResponse[int](
                    label=(
                        (record.surname or "")
                        + " "
                        + (record.name or "")
                        + " "
                        + (record.patronymic or "")
                    ).strip(),
                    value=record.id_employee,
                )
            )
        return result

    async def update(
        self, id_entity: int, update_dto: EmployeeUpdate
    ) -> Employee | None:
        upd_obj = await self.get_by_id(id_entity)
        for k, v in update_dto.model_dump().items():
            setattr(upd_obj, k, v)
        await self.db.flush()
        await self.db.refresh(upd_obj)
        return upd_obj

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True


def get_repository(db: AsyncSession) -> EmployeeRepository:
    return EmployeeRepository(db)
