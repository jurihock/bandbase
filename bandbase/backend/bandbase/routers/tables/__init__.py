from fastapi import APIRouter

from .contacts import router as contacts
from .gigs import router as gigs
from .scores import router as scores


router = APIRouter(prefix='/table', tags=['tables'])

router.include_router(contacts)
router.include_router(gigs)
router.include_router(scores)
