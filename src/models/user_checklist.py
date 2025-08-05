from sqlalchemy import Column, Integer, ForeignKey
from src.core.database import Base
from src.models.checklist import Checklist
from src.models.user import User

class UserChecklist(Base):
    __tablename__ = "t_user_checklist"
    _table_args_ = {"schema": "checklist"}

    id_user_checklist = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(Checklist.id_checklist))
    id_checklist = Column(Integer, ForeignKey(User.id_user))
