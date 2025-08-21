from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.store_employee import StoreEmployeeRepository
from src.schemas import (
    StoreEmployeeCreate,
    StoreEmployeeResponse,
    StoreEmployeeFullResponse,
)
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/store_employees", tags=["StoreEmployee"])


@router.post("/", response_model=StoreEmployeeResponse)
@auth_service.check_roles(["admin"])
async def create_store_employee(
    request: Request,
    store_employee: StoreEmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = StoreEmployeeRepository(db)
    obj = await repo.create(store_employee)
    await db.commit()
    return obj


@router.post("/get_full", response_model=list[StoreEmployeeFullResponse])
async def get_full(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreEmployeeRepository(db)
    return await repo.get_all_full()


@router.get("/", response_model=list[StoreEmployeeResponse])
async def read_store_employees(request: Request, db: AsyncSession = Depends(get_db)):
    repo = StoreEmployeeRepository(db)
    return await repo.get_all()


@router.get("/{store_employee_id}", response_model=StoreEmployeeResponse)
async def read_store_employee(
    request: Request, store_employee_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreEmployeeRepository(db)
    store_employee = await repo.get_by_id(store_employee_id)
    if not store_employee:
        raise HTTPException(status_code=404, detail="store_employee not found")
    return store_employee


@router.delete("/{store_employee_id}")
@auth_service.check_roles(["admin"])
async def delete_store_employee(
    request: Request, store_employee_id: int, db: AsyncSession = Depends(get_db)
):
    repo = StoreEmployeeRepository(db)
    success = await repo.delete(store_employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="store_employee not found")
    await db.commit()
    return {"message": "store_employee deleted"}
