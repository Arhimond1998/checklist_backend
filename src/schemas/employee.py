from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None


class EmployeeCreate(EmployeeBase): ...


class EmployeeUpdate(EmployeeBase): ...


class EmployeeResponse(BaseModel):
    id_employee: int
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None

    model_config = ConfigDict(from_attributes=True)
