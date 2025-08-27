from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserRole, User, Role
from src.schemas import UserRoleCreate, UserRoleUpdate, UserRoleFullResponse
from src.repositories.base import RepositoryBase


class UserRoleRepository(RepositoryBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, create_dto: UserRoleCreate) -> UserRole:
        new_obj = UserRole(**create_dto.model_dump())
        if create_dto.id_user == 1:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "admin change role forbidden"
            )

        for r in await self.db.scalars(
            select(UserRole).where(UserRole.id_user == create_dto.id_user)
        ):
            await self.db.delete(r)

        self.db.add(new_obj)
        await self.db.flush()
        await self.db.refresh(new_obj)
        return new_obj

    async def get_by_id(self, id_user_role: int) -> UserRoleFullResponse | None:
        result = await self.db.execute(
            select(
                UserRole.id_user_role,
                UserRole.id_user,
                UserRole.id_role,
                User.login,
                User.name,
                User.surname,
                User.patronymic,
                Role.code.label("code_role"),
                Role.name.label("name_role"),
            )
            .select_from(UserRole)
            .join(User, User.id_user == UserRole.id_user)
            .join(Role, Role.id_role == UserRole.id_role)
            .where(UserRole.id_user_role == id_user_role)
        )
        record = result.fetchone()
        if record:
            return UserRoleFullResponse(**record._asdict())

    async def get_all(self) -> list[UserRoleFullResponse]:
        result = await self.db.execute(
            select(
                UserRole.id_user_role,
                UserRole.id_user,
                UserRole.id_role,
                User.login,
                User.name,
                User.patronymic,
                User.mail,
                User.surname,
                Role.code.label("code_role"),
                Role.name.label("name_role"),
            )
            .select_from(UserRole)
            .join(User, User.id_user == UserRole.id_user)
            .join(Role, Role.id_role == UserRole.id_role)
        )
        return [UserRoleFullResponse(**r._asdict()) for r in result.fetchall()]

    async def delete(self, id_user_role: int) -> bool:
        checklist = await self.get_by_id(id_user_role)
        if checklist:
            await self.db.delete(checklist)
        await self.db.flush()
        return True
