from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str
    code: str
    id_parent: int | None = None


class RoleCreate(RoleBase): ...


class RoleUpdate(RoleCreate): ...


class RoleResponse(BaseModel):
    id_role: int
    name: str
    code: str
    id_parent: int | None = None
    model_config = ConfigDict(from_attributes=True)
