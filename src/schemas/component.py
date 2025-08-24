from pydantic import BaseModel, ConfigDict


class ComponentBase(BaseModel):
    name: str
    code: str


class ComponentCreate(ComponentBase): ...


class ComponentUpdate(ComponentCreate): ...


class ComponentResponse(BaseModel):
    id_component: int
    name: str
    code: str
    model_config = ConfigDict(from_attributes=True)
