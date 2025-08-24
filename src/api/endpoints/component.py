from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.component import ComponentRepository
from src.schemas import (
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
    ComboboxResponse,
)
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/components", tags=["Component"])


@router.post("/", response_model=ComponentResponse)
@auth_service.check_roles(["admin"])
async def create_component(
    request: Request, component: ComponentCreate, db: AsyncSession = Depends(get_db)
):
    repo = ComponentRepository(db)
    obj = await repo.create(component)
    await db.commit()
    return obj


@router.get("/", response_model=list[ComponentResponse])
async def read_components(db: AsyncSession = Depends(get_db)):
    repo = ComponentRepository(db)
    return await repo.get_all()


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(request: Request, db: AsyncSession = Depends(get_db)):
    component_repo = ComponentRepository(db)
    return await component_repo.get_combo()


@router.get("/{component_id}", response_model=ComponentResponse)
async def read_component(component_id: int, db: AsyncSession = Depends(get_db)):
    repo = ComponentRepository(db)
    component = await repo.get_by_id(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="component not found")
    return component


@router.put("/{component_id}", response_model=ComponentResponse)
@auth_service.check_roles(["admin"])
async def update_component(
    request: Request,
    component_id: int,
    component: ComponentUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = ComponentRepository(db)
    updated_component = await repo.update(component_id, component)
    if not updated_component:
        raise HTTPException(status_code=404, detail="component not found")
    await db.commit()
    return updated_component


@router.delete("/{component_id}")
@auth_service.check_roles(["admin"])
async def delete_component(
    request: Request, component_id: int, db: AsyncSession = Depends(get_db)
):
    repo = ComponentRepository(db)
    success = await repo.delete(component_id)
    if not success:
        raise HTTPException(status_code=404, detail="component not found")
    await db.commit()
    return {"message": "component deleted"}
