from pydantic import BaseModel, ConfigDict


class RoleChecklistBase(BaseModel):
    name_role: str
    code_role: str
    title: str


class RoleChecklistCreate(BaseModel):
    id_role: int
    id_checklist: int


class RoleChecklistResponse(BaseModel):
    id_role_checklist: int
    id_checklist: int
    id_role: int

    model_config = ConfigDict(from_attributes=True)


class RoleChecklistFullResponse(RoleChecklistBase):
    id_role_checklist: int
    id_role: int
    id_checklist: int

    model_config = ConfigDict(from_attributes=True)
