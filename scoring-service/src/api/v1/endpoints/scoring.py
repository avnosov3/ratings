from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.client import StatusCodeNotOKError
from src.schemas.scoring import ScoreFilterDependancy
from src.services.scoring import LogarithmError, ScoreNotFoundError, ScoreServiceDependancy

from . import ERROR_RESPONSE

router = APIRouter()


@router.get(
    "/{accommodation_id}",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {"score_name": 8.32},
                },
            },
        },
        status.HTTP_404_NOT_FOUND: ERROR_RESPONSE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: ERROR_RESPONSE,
        status.HTTP_503_SERVICE_UNAVAILABLE: ERROR_RESPONSE,
    },
    summary="if score_aspect is not provided, general_score will be computed",
)
async def get_score(
    accommodation_id: UUID,
    score_filter: ScoreFilterDependancy,
    score_service: ScoreServiceDependancy,
) -> dict:
    try:
        score_aspect = score_filter.score_aspect
        if score_aspect is not None:
            return await score_service.get_score_aspect(accommodation_id, score_aspect.value)
        return await score_service.get_general_score(accommodation_id)
    except ScoreNotFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error))
    except LogarithmError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))
    except (StatusCodeNotOKError, ConnectionError) as error:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(error))
    except Exception as error:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, f"Unexpected error: {error}")
