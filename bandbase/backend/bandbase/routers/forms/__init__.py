from fastapi import APIRouter

from .contacts import router as contacts


router = APIRouter(prefix='/form', tags=['forms'])

router.include_router(contacts)
