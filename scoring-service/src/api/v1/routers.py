from fastapi import APIRouter

from .endpoints.scoring import router as scoring_router

router = APIRouter()
router.include_router(
    scoring_router,
    prefix="/scoring",
    tags=["scoring"],
)
