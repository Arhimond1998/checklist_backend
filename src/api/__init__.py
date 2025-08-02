from fastapi.routing import APIRouter
from endpoints import checklist
from endpoints import constructor

router = APIRouter('/api')

router.include_router(checklist.router)
router.include_router(constructor.router)