from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    login: str
    password: str


class UserCreate(UserBase): ...


class UserUpdate(BaseModel): 
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None

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
    roles: list[str] | None = None
    components: list[str] | None = None

class UserResponse(BaseModel):
    id_user: int
    name: str
    surname: str | None = None
    patronymic: str | None = None
    mail: str | None = None
    login: str

    model_config = ConfigDict(from_attributes=True)
