from pydantic import BaseModel, ConfigDict


class ChecklistBase(BaseModel):
    title: str
    data: dict


class ChecklistCreate(ChecklistBase):
    id_store: list[int]


class ChecklistUpdate(ChecklistCreate): ...


class ChecklistResponse(ChecklistBase):
    id_checklist: int
    model_config = ConfigDict(from_attributes=True)


class ChecklistTitlesResponse(BaseModel):
    id_checklist: int
    title: str
