from datetime import datetime
from pydantic import BaseModel


class ChecklistUserReportBase(BaseModel):
    id_checklist: int
    id_user: int
    max_score: int
    score: int
    data: dict
    dt: datetime = datetime.now()


class ChecklistUserReportTitle(BaseModel):
    id_checklist_user_report: int
    id_checklist: int
    id_user: int
    score: int
    max_score: int
    dt: datetime
    title: str
    user_fullname: str


class ChecklistUserReportFull(ChecklistUserReportTitle):
    data: dict


class ChecklistUserReportCreate(BaseModel):
    id_checklist: int
    max_score: int
    score: int
    data: dict


class ChecklistUserReportUpdate(ChecklistUserReportCreate):
    id_checklist_user_report: int
