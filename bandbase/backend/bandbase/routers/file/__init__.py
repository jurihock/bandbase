from fastapi import APIRouter

from .contact import router as contact

router = APIRouter(prefix='/file', tags=['file'])

router.include_router(contact)
