from fastapi.routing import APIRouter
from src.api.endpoints import checklist
from src.api.endpoints import user

router = APIRouter(prefix='/api')

router.include_router(checklist.router)
router.include_router(user.router)