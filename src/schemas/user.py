from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    login: str
    password: str


class UserCreate(UserBase): ...


class UserUpdate(UserBase): ...

class UserLogin(BaseModel):
    login: str
    password: str


class UserResponseLogin(BaseModel):
    id_user: int
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    login: str
    access_token: str

class UserResponse(BaseModel):
    id_user: int
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    login: str

    model_config = ConfigDict(from_attributes=True)
