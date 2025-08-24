from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Component(Base):
    __tablename__ = "t_component"
    _table_args_ = {"schema": "checklist"}

    id_component = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    code = Column(String(255), index=True, unique=True)

