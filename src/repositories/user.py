from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, UserRole, Role, Component, RoleComponent
from src.schemas import UserCreate, UserUpdate, ComboboxResponse
from src.deps.database import get_db


class UserNotFound(Exception): ...


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        new_user = User(**user.model_dump())
        self.db.add(new_user)
        await self.db.flush()
        await self.db.refresh(new_user)
        return new_user

    async def get_by_id(self, id_user: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id_user == id_user))
        return result.scalar_one_or_none()

    async def get_combo(self) -> list[ComboboxResponse[int]]:
        result = []
        for record in (await self.db.execute(select(User))).scalars().all():
            result.append(
                ComboboxResponse[int](
                    label=(
                        (record.surname or "")
                        + " "
                        + (record.name or "")
                        + " "
                        + (record.patronymic or "")
                    ).strip(),
                    value=record.id_user,
                )
            )
        return result

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.login == login))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def update(self, id_user: int, user_update: UserUpdate) -> User | None:
        user = await self.get_by_id(id_user)
        for k, v in user_update.model_dump().items():
            setattr(user, k, v)
        await self.db.flush()
        return user

    async def get_roles(self, id_user: int) -> list[str]:
        return (
            (
                await self.db.execute(
                    select(Role.code)
                    .select_from(UserRole)
                    .join(Role, Role.id_role == UserRole.id_role)
                    .where(UserRole.id_user == id_user)
                )
            )
            .scalars()
            .all()
        )
        
    async def get_components(self, id_user: int) -> list[str]:
        return (
            (
                await self.db.execute(
                    select(Component.code)
                    .select_from(UserRole)
                    .join(RoleComponent, UserRole.id_role == RoleComponent.id_role)
                    .join(Component, Component.id_component == RoleComponent.id_component)
                    .where(UserRole.id_user == id_user)
                )
            )
            .scalars()
            .all()
        )


    async def delete(self, id_user: int) -> bool:
        User = await self.get_by_id(id_user)
        await self.db.delete(User)
        await self.db.flush()
        return True

    async def get_password_hash_for_user(self, login: str) -> str:
        user = (
            await self.db.execute(select(User).where(User.login == login))
        ).scalar_one_or_none()
        if not user:
            raise UserNotFound("No user")
        return user.password

    async def set_password_hash_for_user(self, login: str, password: str):
        user = (
            await self.db.execute(select(User).where(User.login == login))
        ).scalar_one_or_none()
        if not user:
            raise UserNotFound("No user")
        user.password = password


def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)
