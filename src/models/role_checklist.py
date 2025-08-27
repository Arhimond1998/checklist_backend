from sqlalchemy import Column, Integer
from src.core.database import Base


class RoleChecklist(Base):
    __tablename__ = "t_role_checklist"
    _table_args_ = {"schema": "checklist"}

    id_role_checklist = Column(Integer, primary_key=True, index=True)
    id_role = Column(Integer, index=True)
    id_checklist = Column(Integer, index=True)
