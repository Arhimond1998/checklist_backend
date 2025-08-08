from sqlalchemy import Column, Integer
from src.core.database import Base


class UserChecklist(Base):
    __tablename__ = "t_user_checklist"
    _table_args_ = {"schema": "checklist"}

    id_user_checklist = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer)
    id_checklist = Column(Integer)
