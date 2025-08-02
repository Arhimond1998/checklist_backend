from pydantic import BaseModel, ConfigDict

class ChecklistBase(BaseModel):
    title: str
    data: dict

class ChecklistCreate(ChecklistBase):
    ...

class ChecklistUpdate(ChecklistBase):
    ...

class ChecklistResponse(BaseModel):
    id_checklist: id
    model_config = ConfigDict(from_attributes=True)