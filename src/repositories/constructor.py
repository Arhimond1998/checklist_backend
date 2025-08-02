from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import TodoItem
from src.schemas import TodoCreate, TodoUpdate

class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, todo: TodoCreate) -> TodoItem:
        new_todo = TodoItem(**todo.model_dump())
        self.db.add(new_todo)
        await self.db.commit()
        await self.db.refresh(new_todo)
        return new_todo

    async def get_by_id(self, todo_id: int) -> TodoItem | None:
        result = await self.db.execute(select(TodoItem).filter(TodoItem.id == todo_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[TodoItem]:
        result = await self.db.execute(select(TodoItem))
        return result.scalars().all()

    async def update(self, todo_id: int, todo: TodoUpdate) -> TodoItem | None:
        stmt = (
            update(TodoItem)
            .where(TodoItem.id == todo_id)
            .values(**todo.model_dump(exclude_unset=True))
            .returning(TodoItem)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, todo_id: int) -> bool:
        stmt = delete(TodoItem).where(TodoItem.id == todo_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0