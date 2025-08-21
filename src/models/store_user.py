from sqlalchemy import Column, Integer
from src.core.database import Base


class StoreUser(Base):
    __tablename__ = "t_store_user"
    _table_args_ = {"schema": "checklist"}

    id_store_user = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, index=True)
    id_store = Column(Integer, index=True)
