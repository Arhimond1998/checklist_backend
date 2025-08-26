from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Checklist
from src.models import UserChecklist
from src.models import User
from src.models import Role
from src.models import UserRole
from src.models import StoreChecklist
from src.models import StoreUser
from src.schemas import ChecklistCreate, ChecklistUpdate, ComboboxResponse


class ChecklistRepository:
    def __init__(self, db: AsyncSession, user: User):
        self.db = db
        self.user = user

    async def create(self, checklist: ChecklistCreate) -> Checklist:
        new_checklist = Checklist(**checklist.model_dump(exclude=["id_store"]))
        self.db.add(new_checklist)
        await self.db.flush()
        await self.db.refresh(new_checklist)
        self.db.add_all(
            [
                StoreChecklist(id_store=r, id_checklist=new_checklist.id_checklist)
                for r in checklist.id_store
            ]
        )
        await self.db.flush()
        return new_checklist

    async def get_by_id(self, id_checklist: int) -> Checklist | None:
        if id_checklist not in await self.get_user_access_checklist():
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")
        result = await self.db.execute(
            select(Checklist).filter(Checklist.id_checklist == id_checklist)
        )
        return result.scalar_one_or_none()

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

    async def update(
        self, id_checklist: int, checklist_update: ChecklistUpdate
    ) -> Checklist | None:
        allowed_checklists = await self.get_user_access_checklist()
        if id_checklist not in allowed_checklists:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нет доступа к чеклисту")

        checklist = await self.get_by_id(id_checklist)
        for k, v in checklist_update.model_dump(exclude=["id_store"]).items():
            setattr(checklist, k, v)
        stmt = select(StoreChecklist).where(StoreChecklist.id_checklist == id_checklist)

        tuples = set((id_checklist, r) for r in checklist_update.id_store)
        existed_tuples = set()
        for r in await self.db.scalars(stmt):
            key = (r.id_checklist, r.id_store)
            if key not in tuples:
                await self.db.delete(r)
            else:
                existed_tuples.add(key)

        self.db.add_all(
            [
                StoreChecklist(id_checklist=t[0], id_store=t[1])
                for t in (tuples - existed_tuples)
            ]
        )

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

        for r in await self.db.scalars(
            select(StoreChecklist).where(StoreChecklist.id_checklist == id_checklist)
        ):
            await self.db.delete(r)

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
                .join(StoreUser, StoreUser.id_store == StoreChecklist.id_store)
                .join(UserRole, UserRole.id_user == StoreUser.id_user)
                .where(UserRole.id_role.in_(roles), StoreUser.id_store.in_(stores))
                .distinct()
            )
        ).all()

        return checklists
