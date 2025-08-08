from pydantic import BaseModel

class UserChecklistBase(BaseModel):
    id_user: int
    id_checklist: int

class UserChecklistCreate(UserChecklistBase):
    ...
