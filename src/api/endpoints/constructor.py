from fastapi import APIRouter, Depends, HTTPException
from src.repositories.checklist import TodoRepository
from src.schemas import TodoCreate, TodoUpdate, TodoResponse
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/todos/", response_model=TodoResponse)
async def create_todo(
    todo: TodoCreate, 
    db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    return await repo.create(todo)

@router.get("/todos/", response_model=list[TodoResponse])
async def read_todos(
    db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    return await repo.get_all()

@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(
    todo_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    todo = await repo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, 
    todo: TodoUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    updated_todo = await repo.update(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    success = await repo.delete(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}