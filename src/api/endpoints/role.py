from fastapi import APIRouter, Depends, HTTPException
from src.repositories.role import RoleRepository
from src.schemas import RoleCreate, RoleUpdate, RoleResponse
from src.deps.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/roles', tags=['Role'])

@router.post("/", response_model=RoleResponse)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    return await repo.create(role)

@router.get("/", response_model=list[RoleResponse])
async def read_roles(
    db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    return await repo.get_all()

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(
    role_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    role = await repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    return role

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int, 
    role: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    updated_role = await repo.update(role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="role not found")
    return updated_role

@router.delete("/{role_id}")
async def delete_role(
    role_id: int, 
    db: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(db)
    success = await repo.delete(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="role not found")
    return {"message": "role deleted"}