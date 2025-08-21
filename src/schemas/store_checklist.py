from pydantic import BaseModel, ConfigDict


class StoreChecklistBase(BaseModel):
    title: str
    name_store: str
    code_store: str


class StoreChecklistCreate(BaseModel):
    id_checklist: int
    id_store: int


class StoreChecklistResponse(BaseModel):
    id_store_checklist: int
    id_checklist: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)

class StoreChecklistFullResponse(StoreChecklistBase):
    id_store_checklist: int
    id_checklist: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)
