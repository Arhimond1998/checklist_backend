from pydantic import BaseModel, ConfigDict


class RoleComponentBase(BaseModel):
    name_role: str
    code_role: str
    name_component: str
    code_component: str


class RoleComponentCreate(BaseModel):
    id_role: int
    id_component: int


class RoleComponentResponse(BaseModel):
    id_role_component: int
    id_role: int
    id_component: int

    model_config = ConfigDict(from_attributes=True)
    
class RoleComponentFullResponse(RoleComponentBase):
    id_role_component: int
    id_role: int
    id_component: int

    model_config = ConfigDict(from_attributes=True)
