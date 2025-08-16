from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from src.core.database import Base


class ChecklistUserReport(Base):
    __tablename__ = "t_checklist_user_report"
    _table_args_ = {"schema": "checklist"}

    id_checklist_user_report = Column(Integer, primary_key=True, index=True)
    id_checklist = Column(Integer)
    id_user = Column(Integer)
    max_score = Column(Integer)
    score = Column(Integer)
    data = Column(JSONB())
    dt = Column(DateTime, default=datetime.now)
