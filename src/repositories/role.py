from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Role
from src.schemas import RoleCreate, RoleUpdate


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: RoleCreate) -> Role:
        new_obj = Role(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_user_role: int) -> Role | None:
        result = await self.db.execute(
            select(Role).filter(Role.id_user_role == id_user_role)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Role]:
        result = await self.db.execute(select(Role))
        return result.scalars().all()

    async def update(self, id_user_role: int, update_dto: RoleUpdate) -> Role | None:
        upd_obj = await self.get_by_id(id_user_role)
        for k, v in update_dto.model_dump().items():
            setattr(upd_obj, k, v)
        await self.db.flush()
        await self.db.refresh(upd_obj)
        return upd_obj

    async def delete(self, id_user_role: int) -> bool:
        checklist = await self.get_by_id(id_user_role)
        if checklist:
            await self.db.delete(checklist)
        await self.db.flush()
        return True
