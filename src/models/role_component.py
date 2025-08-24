from sqlalchemy import Column, Integer
from src.core.database import Base


class RoleComponent(Base):
    __tablename__ = "t_role_component"
    _table_args_ = {"schema": "checklist"}

    id_role_component = Column(Integer, primary_key=True, index=True)
    id_role = Column(Integer, index=True)
    id_component = Column(Integer, index=True)
