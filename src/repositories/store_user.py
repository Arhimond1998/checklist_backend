from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import StoreUser, User, Store
from src.schemas import StoreUserCreate, StoreUserFullResponse


class StoreUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: StoreUserCreate) -> StoreUser:
        new_obj = StoreUser(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> StoreUser | None:
        result = await self.db.execute(
            select(StoreUser).filter(StoreUser.id_store_user == id_entity)
        )
        return result.scalar_one_or_none()
    
    async def get_all_full(self) -> list[StoreUserFullResponse]:
        result = await self.db.execute(
            select(
                StoreUser.id_store_user,
                StoreUser.id_store,
                StoreUser.id_user,
                User.name,
                User.surname,
                User.patronymic,
                User.mail,
                Store.name.label("name_store"),
                Store.code.label("code_store"),
            )
            .select_from(StoreUser)
            .join(User, User.id_user == StoreUser.id_user)
            .join(Store, Store.id_store == StoreUser.id_store)
        )
        return [
            StoreUserFullResponse(
                name=r.name,
                surname=r.surname,
                patronymic=r.patronymic,
                mail=r.mail,
                name_store=r.name_store,
                code_store=r.code_store,
                id_store_user=r.id_store_user,
                id_user=r.id_user,
                id_store=r.id_store,
            )
            for r in result.fetchall()
        ]

    async def get_all(self) -> list[StoreUser]:
        result = await self.db.execute(select(StoreUser))
        return result.scalars().all()

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
