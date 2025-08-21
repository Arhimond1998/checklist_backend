from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Employee(Base):
    __tablename__ = "t_employee"
    _table_args_ = {"schema": "checklist"}

    id_employee = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))
    mail = Column(String(150))
