from datetime import datetime
from pydantic import BaseModel


class ChecklistUserReportBase(BaseModel):
    id_checklist: int
    id_user: int
    max_score: int
    score: int
    data: dict
    dt: datetime = datetime.now()


class ChecklistUserReportCreate(BaseModel): 
    id_checklist: int
    max_score: int
    score: int
    data: dict


class ChecklistUserReportUpdate(ChecklistUserReportCreate):
    id_checklist_user_report: int
