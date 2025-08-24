from sqlalchemy import Column, Integer, String
from src.core.database import Base


class User(Base):
    __tablename__ = "t_user"
    _table_args_ = {"schema": "checklist"}

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))
    mail = Column(String(150))

    login = Column(String(150), unique=True)
    password = Column(String(150))
