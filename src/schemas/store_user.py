from pydantic import BaseModel, ConfigDict


class StoreUserBase(BaseModel):
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    name_store: str
    code_store: str


class StoreUserCreate(BaseModel):
    id_user: int
    id_store: int


class StoreUserResponse(BaseModel):
    id_store_user: int
    id_user: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)


class StoreUserFullResponse(StoreUserBase):
    id_store_user: int
    id_user: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)
