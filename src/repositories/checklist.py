from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Checklist
from src.models import UserChecklist
from src.schemas import ChecklistCreate, ChecklistUpdate, ComboboxResponse


class ChecklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, checklist: ChecklistCreate) -> Checklist:
        new_checklist = Checklist(**checklist.model_dump())
        self.db.add(new_checklist)
        await self.db.flush()
        await self.db.refresh(new_checklist)
        return new_checklist

    async def get_by_id(self, id_checklist: int) -> Checklist | None:
        result = await self.db.execute(
            select(Checklist).filter(Checklist.id_checklist == id_checklist)
        )
        return result.scalar_one_or_none()
    
    async def get_combo(self) -> list[ComboboxResponse[int]]:
        result = []
        for record in (await self.db.execute(select(Checklist))).scalars().all():
            result.append(
                ComboboxResponse[int](
                    label=record.title,
                    value=record.id_checklist,
                )
            )
        return result

    async def get_all(self) -> list[Checklist]:
        result = await self.db.execute(select(Checklist))
        return result.scalars().all()

    async def update(
        self, id_checklist: int, checklist_update: ChecklistUpdate
    ) -> Checklist | None:
        checklist = await self.get_by_id(id_checklist)
        for k, v in checklist_update.model_dump().items():
            setattr(checklist, k, v)
        await self.db.flush()
        await self.db.refresh(checklist)
        return checklist

    async def delete(self, id_checklist: int) -> bool:
        checklist = await self.get_by_id(id_checklist)
        if checklist:
            await self.db.delete(checklist)

        user_checklist = (
            await self.db.execute(
                select(UserChecklist).where(UserChecklist.id_checklist == id_checklist)
            )
        ).scalar_one_or_none()
        if user_checklist:
            await self.db.delete(user_checklist)
        await self.db.flush()
        return True
