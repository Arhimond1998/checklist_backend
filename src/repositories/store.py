from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Store
from src.schemas import StoreCreate, StoreUpdate, ComboboxResponse


class StoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: StoreCreate) -> Store:
        new_obj = Store(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> Store | None:
        result = await self.db.execute(
            select(Store).filter(Store.id_store == id_entity)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Store]:
        result = await self.db.execute(select(Store))
        return result.scalars().all()

    async def get_combo(self) -> list[ComboboxResponse[int]]:
        result = []
        for record in (await self.db.execute(select(Store))).scalars().all():
            result.append(
                ComboboxResponse[int](
                    label=(
                        (record.name or "") + " (" + (record.code or "") + ")"
                    ).strip(),
                    value=record.id_store,
                )
            )
        return result

    async def update(self, id_entity: int, update_dto: StoreUpdate) -> Store | None:
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
