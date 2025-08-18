from fastapi import Depends
from fastapi.routing import APIRouter

from src.deps.auth import check_token
from src.api.endpoints import checklist
from src.api.endpoints import checklist_user_report
from src.api.endpoints import user
from src.api.endpoints import auth
from src.api.endpoints import role
from src.api.endpoints import user_role

auth_router = APIRouter(prefix="/api")
auth_router.include_router(auth.router)

web_router = APIRouter(prefix="/api", dependencies=[Depends(check_token)])

web_router.include_router(checklist.router)
web_router.include_router(checklist_user_report.router)
web_router.include_router(user.router)
web_router.include_router(role.router)
web_router.include_router(user_role.router)
