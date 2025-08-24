from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.role import RoleRepository
from src.schemas import RoleCreate, RoleUpdate, RoleResponse, ComboboxResponse, ComboboxTreeResponse
from src.deps.database import get_db
from src.services.auth import auth_service

router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("/", response_model=RoleResponse)
@auth_service.check_roles(["admin"])
async def create_role(
    request: Request, role: RoleCreate, db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    obj = await repo.create(role)
    await db.commit()
    return obj


@router.get("/", response_model=list[RoleResponse])
async def read_roles(db: AsyncSession = Depends(get_db)):
    repo = RoleRepository(db)
    return await repo.get_all()


@router.post("/combobox", response_model=list[ComboboxResponse[int]])
async def get_combobox(request: Request, db: AsyncSession = Depends(get_db)):
    role_repo = RoleRepository(db)
    return await role_repo.get_combo()

@router.post("/tree_combobox", response_model=list[ComboboxTreeResponse[int]])
async def get_tree_combobox(request: Request, db: AsyncSession = Depends(get_db)):
    role_repo = RoleRepository(db)
    return await role_repo.get_tree_combo()


@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(role_id: int, db: AsyncSession = Depends(get_db)):
    repo = RoleRepository(db)
    role = await repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    return role


@router.put("/{role_id}", response_model=RoleResponse)
@auth_service.check_roles(["admin"])
async def update_role(
    request: Request, role_id: int, role: RoleUpdate, db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    updated_role = await repo.update(role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="role not found")
    await db.commit()
    return updated_role


@router.delete("/{role_id}")
@auth_service.check_roles(["admin"])
async def delete_role(
    request: Request, role_id: int, db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    success = await repo.delete(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="role not found")
    if role_id == 1:
        raise HTTPException(status_code=403, detail="cant delete admin role")
    await db.commit()
    return {"message": "role deleted"}
