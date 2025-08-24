from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import StoreChecklist, Checklist, Store
from src.schemas import StoreChecklistCreate, StoreChecklistFullResponse


class StoreChecklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: StoreChecklistCreate) -> StoreChecklist:
        new_obj = StoreChecklist(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> StoreChecklist | None:
        result = await self.db.execute(
            select(StoreChecklist).filter(StoreChecklist.id_store_checklist == id_entity)
        )
        return result.scalar_one_or_none()
    
    async def get_all_full(self) -> list[StoreChecklistFullResponse]:
        result = await self.db.execute(
            select(
                StoreChecklist.id_store_checklist,
                StoreChecklist.id_store,
                StoreChecklist.id_checklist,
                Checklist.title,
                Store.name.label("name_store"),
                Store.code.label("code_store"),
            )
            .select_from(StoreChecklist)
            .join(Checklist, Checklist.id_checklist == StoreChecklist.id_checklist)
            .join(Store, Store.id_store == StoreChecklist.id_store)
        )
        return [
            StoreChecklistFullResponse(
                title=r.title,
                name_store=r.name_store,
                code_store=r.code_store,
                id_store_checklist=r.id_store_checklist,
                id_checklist=r.id_checklist,
                id_store=r.id_store,
            )
            for r in result.fetchall()
        ]

    async def get_all(self) -> list[StoreChecklist]:
        result = await self.db.execute(select(StoreChecklist))
        return result.scalars().all()

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
