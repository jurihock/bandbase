from fastapi import APIRouter

from .contact import router as contact

router = APIRouter(prefix='/form', tags=['form'])

router.include_router(contact)
