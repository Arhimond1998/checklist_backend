from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Role(Base):
    __tablename__ = "t_role"
    _table_args_ = {"schema": "checklist"}

    id_role = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    code = Column(String(255), index=True)
