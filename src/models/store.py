from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Store(Base):
    __tablename__ = "t_store"
    _table_args_ = {"schema": "checklist"}

    id_store = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    code = Column(String(255), index=True)
    address = Column(String(255))
    
