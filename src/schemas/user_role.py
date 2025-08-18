from pydantic import BaseModel, ConfigDict


class UserRoleBase(BaseModel):
    id_user: int
    id_role: int


class UserRoleCreate(UserRoleBase): ...


class UserRoleUpdate(UserRoleBase):
    id_user_role: int


class UserRoleResponse(BaseModel):
    id_user: int
    id_role: str
    code_role: str
    name_role: str
    login: str

    model_config = ConfigDict(from_attributes=True)
