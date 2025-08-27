from pydantic import BaseModel, ConfigDict


class UserRoleBase(BaseModel):
    id_user: int
    id_role: int


class UserRoleCreate(UserRoleBase): ...


class UserRoleUpdate(UserRoleBase):
    id_user_role: int


class UserRoleResponse(BaseModel):
    id_user_role: int
    id_user: int
    id_role: int

    model_config = ConfigDict(from_attributes=True)


class UserRoleFullResponse(BaseModel):
    id_user_role: int
    id_user: int
    id_role: int
    code_role: str
    name_role: str
    login: str
    name: str
    surname: str | None = None
    patronymic: str | None = None
