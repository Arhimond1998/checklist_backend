from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class ComboboxResponse(BaseModel, Generic[T]):
    label: str
    value: T


class ComboboxTreeResponse(BaseModel, Generic[T]):
    name: str
    id: T
    id_parent: T | None = None
