from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.auth import get_current_user

from src.models import Checklist
from src.models import UserChecklist
from src.models import User
from src.models import Store
from src.models import Role
from src.models import UserRole
from src.models import StoreChecklist
from src.models import RoleChecklist
from src.models import StoreUser
from src.schemas import (
    ChecklistCreate,
    ChecklistUpdate,
    ComboboxResponse,
    ChecklistResponse,
    ChecklistFullResponse,
    Filters,
)
from src.repositories.base import RepositoryBase


class ChecklistRepository(RepositoryBase):
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user

    async def create(self, checklist: ChecklistCreate) -> Checklist:
        new_checklist = Checklist(
            **checklist.model_dump(exclude=["id_store", "id_role"])
        )
        self.db.add(new_checklist)
        await self.db.flush()
        await self.db.refresh(new_checklist)
        self.db.add_all(
            [
                RoleChecklist(
                    id_role=checklist.id_role, id_checklist=new_checklist.id_checklist
                ),
                StoreChecklist(
                    id_store=checklist.id_store, id_checklist=new_checklist.id_checklist
                ),
            ]
        )
        await self.db.flush()
        return new_checklist

    async def get_by_id_info(self, id_checklist: int) -> ChecklistResponse:
        if id_checklist not in await self.get_user_access_checklist():
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")
        result = (
            await self.db.execute(
                select(
                    Checklist.id_checklist,
                    Checklist.title,
                    Checklist.data,
                    StoreChecklist.id_store,
                    RoleChecklist.id_role,
                )
                .select_from(Checklist)
                .outerjoin(
                    StoreChecklist,
                    StoreChecklist.id_checklist == Checklist.id_checklist,
                )
                .outerjoin(
                    RoleChecklist, RoleChecklist.id_checklist == Checklist.id_checklist
                )
                .filter(Checklist.id_checklist == id_checklist)
            )
        ).fetchone()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        return ChecklistResponse(**result._asdict())

    async def get_by_id(self, id_checklist: int) -> Checklist | None:
        if id_checklist not in await self.get_user_access_checklist():
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")
        result = (
            await self.db.execute(
                select(Checklist).filter(Checklist.id_checklist == id_checklist)
            )
        ).scalar_one_or_none()
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        return result

    async def get_combo(self) -> list[ComboboxResponse[int]]:
        result: list[ComboboxResponse[int]] = []
        allowed_checklists = await self.get_user_access_checklist()
        for record in (await self.db.execute(select(Checklist))).scalars().all():
            if record.id_checklist not in allowed_checklists:
                continue
            result.append(
                ComboboxResponse[int](
                    label=record.title,
                    value=record.id_checklist,
                )
            )

        return result

    async def get_all(self) -> list[Checklist]:
        result = (await self.db.execute(select(Checklist))).scalars().all()
        allowed_checklists = await self.get_user_access_checklist()
        return [r for r in result if r.id_checklist in allowed_checklists]

    async def get_all_titles_expanded(
        self, filters: Filters
    ) -> list[ChecklistFullResponse]:
        allowed_checklists = await self.get_user_access_checklist()
        if not allowed_checklists:
            return []
        stmt = self.apply_filters(
            (
                select(
                    Checklist.id_checklist,
                    Checklist.title,
                    Checklist.data,
                    Store.id_store,
                    Store.name.label("name_store"),
                    Store.code.label("code_store"),
                    Role.id_role,
                    Role.name.label("name_role"),
                    Role.code.label("code_role"),
                )
                .select_from(Checklist)
                .outerjoin(
                    StoreChecklist,
                    StoreChecklist.id_checklist == Checklist.id_checklist,
                )
                .outerjoin(Store, Store.id_store == StoreChecklist.id_store)
                .outerjoin(
                    RoleChecklist, RoleChecklist.id_checklist == Checklist.id_checklist
                )
                .outerjoin(Role, Role.id_role == RoleChecklist.id_role)
                .where(Checklist.id_checklist.in_(allowed_checklists))
            ),
            filters,
        )
        result = (await self.db.execute(stmt)).fetchall()

        return [ChecklistFullResponse(**r._asdict()) for r in result]

    async def update(
        self, id_checklist: int, checklist_update: ChecklistUpdate
    ) -> Checklist | None:
        allowed_checklists = await self.get_user_access_checklist()
        if id_checklist not in allowed_checklists:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")

        checklist = await self.get_by_id(id_checklist)
        for k, v in checklist_update.model_dump(
            exclude=["id_store", "id_role"]
        ).items():
            setattr(checklist, k, v)
        store_record = await self.db.scalar(
            select(StoreChecklist).where(StoreChecklist.id_checklist == id_checklist)
        )
        role_record = await self.db.scalar(
            select(RoleChecklist).where(RoleChecklist.id_checklist == id_checklist)
        )

        store_record.id_store = checklist_update.id_store
        role_record.id_role = checklist_update.id_role

        await self.db.flush()
        await self.db.refresh(checklist)
        return checklist

    async def delete(self, id_checklist: int) -> bool:
        allowed_checklists = await self.get_user_access_checklist()
        if id_checklist not in allowed_checklists:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")

        checklist = await self.get_by_id(id_checklist)
        if checklist:
            await self.db.delete(checklist)

        store_record = await self.db.scalar(
            select(StoreChecklist).where(StoreChecklist.id_checklist == id_checklist)
        )
        role_record = await self.db.scalar(
            select(RoleChecklist).where(RoleChecklist.id_checklist == id_checklist)
        )
        await self.db.delete(store_record)
        await self.db.delete(role_record)

        user_checklist = (
            await self.db.execute(
                select(UserChecklist).where(UserChecklist.id_checklist == id_checklist)
            )
        ).scalar_one_or_none()
        if user_checklist:
            await self.db.delete(user_checklist)
        await self.db.flush()
        return True

    async def get_user_access_checklist(self) -> list[int]:
        if self.user.id_user == 1:
            return (await self.db.scalars(select(Checklist.id_checklist))).all()
        
        id_role = await self.db.scalar(
            select(UserRole.id_role).where(UserRole.id_user == self.user.id_user)
        )
        # Define the recursive CTE
        with_manager = (
            select(
                Role.id_role,
                Role.id_parent,
            )
            .where(Role.id_role == id_role)
            .cte(name="with_role", recursive=True)
        )

        # Define the recursive member
        recursive_role = select(Role.id_role, Role.id_parent).join(
            with_manager, Role.id_parent == with_manager.c.id_role
        )

        recursive_cte = with_manager.union_all(recursive_role)
        roles = (await self.db.scalars(select(recursive_cte.c.id_role))).all()
        stores = (
            await self.db.scalars(
                select(StoreUser.id_store).where(StoreUser.id_user == self.user.id_user)
            )
        ).all()

        checklists = (
            await self.db.scalars(
                select(Checklist.id_checklist)
                .select_from(Checklist)
                .join(
                    StoreChecklist,
                    StoreChecklist.id_checklist == Checklist.id_checklist,
                )
                .join(
                    RoleChecklist, RoleChecklist.id_checklist == Checklist.id_checklist
                )
                .where(RoleChecklist.id_role.in_(roles), StoreChecklist.id_store.in_(stores))
                .distinct()
            )
        ).all()

        return checklists


def get_repository(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return ChecklistRepository(db, current_user)
