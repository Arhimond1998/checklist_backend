from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import RoleComponent, Role, Component
from src.schemas import RoleComponentCreate, RoleComponentFullResponse


class RoleComponentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: RoleComponentCreate) -> RoleComponent:
        new_obj = RoleComponent(**create_dto.model_dump())
        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_entity: int) -> RoleComponent | None:
        result = await self.db.execute(
            select(RoleComponent).filter(RoleComponent.id_role_component == id_entity)
        )
        return result.scalar_one_or_none()

    async def get_all_full(self) -> list[RoleComponentFullResponse]:
        result = await self.db.execute(
            select(
                RoleComponent.id_role_component,
                RoleComponent.id_component,
                RoleComponent.id_role,
                Role.name.label("name_role"),
                Role.code.label("code_role"),
                Component.name.label("name_component"),
                Component.code.label("code_component"),
            )
            .select_from(RoleComponent)
            .join(Role, Role.id_role == RoleComponent.id_role)
            .join(Component, Component.id_component == RoleComponent.id_component)
        )
        return [
            RoleComponentFullResponse(
                name_component=r.name_component,
                code_component=r.code_component,
                name_role=r.name_role,
                code_role=r.code_role,
                id_role_component=r.id_role_component,
                id_role=r.id_role,
                id_component=r.id_component,
            )
            for r in result.fetchall()
        ]

    async def get_all(self) -> list[RoleComponent]:
        result = await self.db.execute(select(RoleComponent))
        return result.scalars().all()

    async def delete(self, id_entity: int) -> bool:
        db_obj = await self.get_by_id(id_entity)
        if db_obj:
            await self.db.delete(db_obj)
        await self.db.flush()
        return True
