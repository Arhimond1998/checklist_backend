from fastapi import Depends
from fastapi.routing import APIRouter

from src.deps.auth import check_token
from src.api.endpoints import checklist
from src.api.endpoints import checklist_user_report
from src.api.endpoints import user
from src.api.endpoints import auth
from src.api.endpoints import role
from src.api.endpoints import user_role
from src.api.endpoints import store
from src.api.endpoints import store_user
from src.api.endpoints import store_employee
from src.api.endpoints import employee
from src.api.endpoints import store_checklist

auth_router = APIRouter(prefix="/api")
auth_router.include_router(auth.router)

web_router = APIRouter(prefix="/api", dependencies=[Depends(check_token)])

web_router.include_router(checklist.router)
web_router.include_router(checklist_user_report.router)
web_router.include_router(user.router)
web_router.include_router(role.router)
web_router.include_router(user_role.router)
web_router.include_router(store.router)
web_router.include_router(store_user.router)
web_router.include_router(store_employee.router)
web_router.include_router(employee.router)
web_router.include_router(store_checklist.router)
