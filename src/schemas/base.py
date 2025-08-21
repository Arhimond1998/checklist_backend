from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class ComboboxResponse(BaseModel, Generic[T]):
    label: str
    value: T
