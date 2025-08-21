from pydantic import BaseModel, ConfigDict


class StoreBase(BaseModel):
    name: str
    code: str
    address: str | None = None


class StoreCreate(StoreBase): ...


class StoreUpdate(StoreCreate): ...


class StoreResponse(StoreBase):
    id_store: int

    model_config = ConfigDict(from_attributes=True)
