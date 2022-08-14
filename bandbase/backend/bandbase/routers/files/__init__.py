from fastapi import APIRouter

from .contacts import router as contacts


router = APIRouter(prefix='/file', tags=['files'])

router.include_router(contacts)
