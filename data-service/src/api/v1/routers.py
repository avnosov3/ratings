from fastapi import APIRouter

from .endpoints.accommodation import router as accommodation_router

router = APIRouter()
router.include_router(
    accommodation_router,
    prefix="/accommodations",
    tags=["accommodations"],
)
