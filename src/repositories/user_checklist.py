from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserChecklist
from src.schemas import UserChecklistCreate


class UserChecklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_checklist: UserChecklistCreate) -> UserChecklist:
        new_user_checklist = UserChecklist(**user_checklist.model_dump())
        self.db.add(new_user_checklist)
        await self.db.flush()
        await self.db.refresh(new_user_checklist)
        return new_user_checklist

    # async def get_by_id(self, id_checklist: int) -> Checklist | None:
    #     result = await self.db.execute(select(Checklist).filter(Checklist.id_checklist == id_checklist))
    #     return result.scalar_one_or_none()

    # async def get_all(self) -> list[Checklist]:
    #     result = await self.db.execute(select(Checklist))
    #     return result.scalars().all()

    # async def update(self, id_checklist: int, checklist_update: ChecklistUpdate) -> Checklist | None:
    #     checklist = await self.get_by_id(id_checklist)
    #     for k, v in checklist_update.model_dump().items():
    #         setattr(checklist, k, v)
    #     await self.db.flush()
    #     return True

    # async def delete(self, id_checklist: int) -> bool:
    #     checklist = await self.get_by_id(id_checklist)
    #     await self.db.delete(checklist)
    #     await self.db.flush()
    #     return True
    