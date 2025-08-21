from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import StoreEmployee, Employee, Store
from src.schemas import StoreEmployeeCreate, StoreEmployeeFullResponse


class StoreEmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: StoreEmployeeCreate) -> StoreEmployee:
        new_obj = StoreEmployee(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> StoreEmployee | None:
        result = await self.db.execute(
            select(StoreEmployee).filter(StoreEmployee.id_store_employee == id_entity)
        )
        return result.scalar_one_or_none()

    async def get_all_full(self) -> list[StoreEmployeeFullResponse]:
        result = await self.db.execute(
            select(
                StoreEmployee.id_store_employee,
                StoreEmployee.id_store,
                StoreEmployee.id_employee,
                Employee.name,
                Employee.surname,
                Employee.patronymic,
                Employee.mail,
                Store.name.label("name_store"),
                Store.code.label("code_store"),
            )
            .select_from(StoreEmployee)
            .join(Employee, Employee.id_employee == StoreEmployee.id_employee)
            .join(Store, Store.id_store == StoreEmployee.id_store)
        )
        return [
            StoreEmployeeFullResponse(
                name=r.name,
                surname=r.surname,
                patronymic=r.patronymic,
                mail=r.mail,
                name_store=r.name_store,
                code_store=r.code_store,
                id_store_employee=r.id_store_employee,
                id_employee=r.id_employee,
                id_store=r.id_store,
            )
            for r in result.fetchall()
        ]

    async def get_all(self) -> list[StoreEmployee]:
        result = await self.db.execute(select(StoreEmployee))
        return result.scalars().all()

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
