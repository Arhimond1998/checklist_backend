from sqlalchemy import Column, Integer
from src.core.database import Base


class StoreEmployee(Base):
    __tablename__ = "t_store_employee"
    _table_args_ = {"schema": "checklist"}

    id_store_employee = Column(Integer, primary_key=True, index=True)
    id_employee = Column(Integer, index=True)
    id_store = Column(Integer, index=True)
