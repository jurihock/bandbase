from fastapi import APIRouter

from .contacts import router as contacts


router = APIRouter(prefix='/list', tags=['lists'])

router.include_router(contacts)
