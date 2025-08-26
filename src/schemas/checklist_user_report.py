from datetime import datetime
from pydantic import BaseModel


class ChecklistUserReportBase(BaseModel):
    id_checklist: int
    id_user: int
    max_score: int
    score: int
    data: dict
    id_employee: int | None = None
    dt: datetime = datetime.now()


class ChecklistUserReportTitle(BaseModel):
    id_checklist_user_report: int
    id_checklist: int
    id_user: int
    id_employee: int | None = None
    id_store: int
    score: int
    max_score: int
    dt: datetime
    title: str
    user_fullname: str
    employee_fullname: str | None = None
    name_store: str
    code_store: str


class ChecklistUserReportFull(ChecklistUserReportTitle):
    data: dict


class ChecklistUserReportCreate(BaseModel):
    id_checklist: int
    id_employee: int
    max_score: int
    score: int
    data: dict


class ChecklistUserReportUpdate(ChecklistUserReportCreate):
    id_checklist_user_report: int
