from sqlalchemy import Column, Integer
from src.core.database import Base


class UserRole(Base):
    __tablename__ = "t_user_role"
    _table_args_ = {"schema": "checklist"}

    id_user_role = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer)
    id_role = Column(Integer)
