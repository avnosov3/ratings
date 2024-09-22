from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.db import AsyncSessionDependency
from src.schemas.accommodation import AccommodationOut, ExpandedAccommodationOut
from src.schemas.review import ReviewOut
from src.services.accommodation import AccommodationServiceDependency
from src.services.review import ReviewServiceDependancy

from . import ERROR_RESPONSE, PaginationDependancy
from .filters import AccommodationFiltersDependency

router = APIRouter()


@router.get(
    "/{accommodation_id}",
    response_model=Union[AccommodationOut, ExpandedAccommodationOut],
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation(
    accommodation_id: UUID,
    *,
    expand: Optional[bool] = False,
    accommodation_service: AccommodationServiceDependency,
    session: AsyncSessionDependency,
) -> Union[AccommodationOut, ExpandedAccommodationOut]:
    args = (accommodation_id, session)
    if expand:
        accommodation = await accommodation_service.get_expanded_accommodation(*args)
    else:
        accommodation = await accommodation_service.get_accommodation(*args)
    if accommodation is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Accommodation with id={accommodation_id} was not found")

    return accommodation


@router.get("", response_model=list[AccommodationOut])
async def get_accommodations(
    pagination: PaginationDependancy,
    accommodation_service: AccommodationServiceDependency,
    session: AsyncSessionDependency,
) -> list[AccommodationOut]:
    return await accommodation_service.get_accommodations(session, **pagination.model_dump())


@router.get(
    "/{accommodation_id}/reviews",
    response_model=list[ReviewOut],
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation_reviews(
    accommodation_id: UUID,
    pagination: PaginationDependancy,
    accommodation_filters: AccommodationFiltersDependency,
    review_service: ReviewServiceDependancy,
    session: AsyncSessionDependency,
) -> list[ReviewOut]:
    return await review_service.get_reviews_by_accommodation(
        accommodation_id,
        session,
        **pagination.model_dump(),
        **accommodation_filters.model_dump(),
    )


@router.get(
    "/{accommodation_id}/reviews/{review_id}",
    response_model=ReviewOut,
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation_review(
    accommodation_id: UUID,
    review_id: UUID,
    review_service: ReviewServiceDependancy,
    session: AsyncSessionDependency,
) -> ReviewOut:
    review = await review_service.get_review_by_accommodation(accommodation_id, review_id, session)
    if review is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Review with id={review_id} was not found in accommodation with id {accommodation_id}",
        )

    return review
