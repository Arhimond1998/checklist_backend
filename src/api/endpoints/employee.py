from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.employee import EmployeeRepository
from src.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    ComboboxResponse,
    Filters,
)
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.post("/", response_model=EmployeeResponse)
@auth_service.check_roles(["admin"])
async def create_employee(
    request: Request, employee: EmployeeCreate, db: AsyncSession = Depends(get_db)
):
    repo = EmployeeRepository(db)
    new_obj = await repo.create(employee)
    await db.commit()
    return new_obj


@router.get("/", response_model=list[EmployeeResponse])
async def read_employees(request: Request, db: AsyncSession = Depends(get_db)):
    repo = EmployeeRepository(db)
    return await repo.get_all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def read_employee(
    request: Request, employee_id: int, db: AsyncSession = Depends(get_db)
):
    repo = EmployeeRepository(db)
    employee = await repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="employee not found")
    return employee


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(
    filters: Filters, request: Request, db: AsyncSession = Depends(get_db)
):
    employee_repo = EmployeeRepository(db)
    return await employee_repo.get_combo(filters)


@router.put("/{employee_id}", response_model=EmployeeResponse)
@auth_service.check_roles(["admin"])
async def update_employee(
    request: Request,
    employee_id: int,
    employee: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = EmployeeRepository(db)
    updated_employee = await repo.update(employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="employee not found")
    await db.commit()
    return updated_employee


@router.delete("/{employee_id}")
@auth_service.check_roles(["admin"])
async def delete_employee(
    request: Request, employee_id: int, db: AsyncSession = Depends(get_db)
):
    repo = EmployeeRepository(db)
    success = await repo.delete(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="employee not found")
    await db.commit()
    return {"message": "employee deleted"}
