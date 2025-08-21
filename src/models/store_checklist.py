from sqlalchemy import Column, Integer
from src.core.database import Base


class StoreChecklist(Base):
    __tablename__ = "t_store_checklist"
    _table_args_ = {"schema": "checklist"}

    id_store_checklist = Column(Integer, primary_key=True, index=True)
    id_checklist = Column(Integer, index=True)
    id_store = Column(Integer, index=True)
