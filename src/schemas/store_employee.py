from pydantic import BaseModel, ConfigDict


class StoreEmployeeBase(BaseModel):
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    name_store: str
    code_store: str


class StoreEmployeeCreate(BaseModel):
    id_employee: int
    id_store: int


class StoreEmployeeResponse(BaseModel):
    id_store_employee: int
    id_employee: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)
    
class StoreEmployeeFullResponse(StoreEmployeeBase):
    id_store_employee: int
    id_employee: int
    id_store: int

    model_config = ConfigDict(from_attributes=True)
