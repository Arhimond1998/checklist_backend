from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.role_component import RoleComponentRepository
from src.schemas import (
    RoleComponentCreate,
    RoleComponentResponse,
    RoleComponentFullResponse,
)
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/role_components", tags=["RoleComponent"])


@router.post("/", response_model=RoleComponentResponse)
@auth_service.check_roles(["admin"])
async def create_role_component(
    request: Request,
    role_component: RoleComponentCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = RoleComponentRepository(db)
    obj = await repo.create(role_component)
    await db.commit()
    return obj


@router.get("/", response_model=list[RoleComponentResponse])
async def read_role_components(request: Request, db: AsyncSession = Depends(get_db)):
    repo = RoleComponentRepository(db)
    return await repo.get_all()


@router.get("/{role_component_id}", response_model=RoleComponentResponse)
async def read_role_component(
    request: Request, role_component_id: int, db: AsyncSession = Depends(get_db)
):
    repo = RoleComponentRepository(db)
    role_component = await repo.get_by_id(role_component_id)
    if not role_component:
        raise HTTPException(status_code=404, detail="role_component not found")
    return role_component


@router.post("/get_full", response_model=list[RoleComponentFullResponse])
async def get_full(request: Request, db: AsyncSession = Depends(get_db)):
    repo = RoleComponentRepository(db)
    return await repo.get_all_full()


@router.delete("/{role_component_id}")
@auth_service.check_roles(["admin"])
async def delete_role_component(
    request: Request, role_component_id: int, db: AsyncSession = Depends(get_db)
):
    repo = RoleComponentRepository(db)
    success = await repo.delete(role_component_id)
    if not success:
        raise HTTPException(status_code=404, detail="role_component not found")
    await db.commit()
    return {"message": "role_component deleted"}
