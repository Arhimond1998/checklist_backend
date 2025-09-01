from pydantic import BaseModel, ConfigDict


class ChecklistBase(BaseModel):
    title: str
    data: dict


class ChecklistCreate(ChecklistBase):
    id_store: int
    id_role: int


class ChecklistUpdate(ChecklistCreate): ...


class ChecklistResponse(ChecklistBase):
    id_checklist: int
    id_store: int | None = None
    id_role: int | None = None
    model_config = ConfigDict(from_attributes=True)


class ChecklistTitlesResponse(BaseModel):
    id_checklist: int
    title: str


class ChecklistFullTitleResponse(BaseModel):
    id_checklist: int
    title: str
    id_store: int | None = None
    id_role: int | None = None
    name_store: str | None = None
    code_store: str | None = None
    name_role: str | None = None
    code_role: str | None = None


class ChecklistFullResponse(ChecklistFullTitleResponse):
    data: dict
