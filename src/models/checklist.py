from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from src.core.database import Base


class Checklist(Base):
    __tablename__ = "t_checklist"
    _table_args_ = {"schema": "checklist"}

    id_checklist = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    data = Column(JSONB())
