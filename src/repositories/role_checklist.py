from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import RoleChecklist, Role, Checklist
from src.schemas import RoleChecklistCreate, RoleChecklistFullResponse


class RoleChecklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: RoleChecklistCreate) -> RoleChecklist:
        new_obj = RoleChecklist(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> RoleChecklist | None:
        result = await self.db.execute(
            select(RoleChecklist).filter(RoleChecklist.id_role_checklist == id_entity)
        )
        return result.scalar_one_or_none()

    async def get_all_full(self) -> list[RoleChecklistFullResponse]:
        result = await self.db.execute(
            select(
                RoleChecklist.id_role_checklist,
                RoleChecklist.id_checklist,
                RoleChecklist.id_role,
                Role.name.label("name_role"),
                Role.code.label("code_role"),
                Checklist.name.label("name_checklist"),
                Checklist.code.label("code_checklist"),
            )
            .select_from(RoleChecklist)
            .join(Role, Role.id_role == RoleChecklist.id_role)
            .join(Checklist, Checklist.id_checklist == RoleChecklist.id_checklist)
        )
        return [
            RoleChecklistFullResponse(
                title=r.title,
                name_role=r.name_role,
                code_role=r.code_role,
                id_role_checklist=r.id_role_checklist,
                id_role=r.id_role,
                id_checklist=r.id_checklist,
            )
            for r in result.fetchall()
        ]

    async def get_all(self) -> list[RoleChecklist]:
        result = await self.db.execute(select(RoleChecklist))
        return result.scalars().all()

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
