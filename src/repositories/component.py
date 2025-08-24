from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Component
from src.schemas import (
    ComponentCreate,
    ComponentUpdate,
    ComboboxResponse,
)


class ComponentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: ComponentCreate) -> Component:
        new_obj = Component(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_component: int) -> Component | None:
        result = await self.db.execute(
            select(Component).filter(Component.id_component == id_component)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Component]:
        result = await self.db.execute(select(Component))
        return result.scalars().all()

    async def get_combo(self) -> list[ComboboxResponse[int]]:
        result = []
        for record in (await self.db.execute(select(Component))).scalars().all():
            result.append(
                ComboboxResponse[int](
                    label=(
                        (record.name or "") + " (" + (record.code or "") + ")"
                    ).strip(),
                    value=record.id_component,
                )
            )
        return result

    async def update(
        self, id_component: int, update_dto: ComponentUpdate
    ) -> Component | None:
        upd_obj = await self.get_by_id(id_component)
        for k, v in update_dto.model_dump().items():
            setattr(upd_obj, k, v)
        await self.db.flush()
        await self.db.refresh(upd_obj)
        return upd_obj

    async def delete(self, id_component: int) -> bool:
        checklist = await self.get_by_id(id_component)
        if checklist:
            await self.db.delete(checklist)
        await self.db.flush()
        return True
