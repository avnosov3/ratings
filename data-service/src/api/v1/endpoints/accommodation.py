from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_async_session
from src.schemas.accommodation import AccommodationOut, ExpandedAccommodationOut
from src.schemas.review import ReviewOut
from src.services.accommodation import AccommodationService, get_accommodation_service
from src.services.review import ReviewService, get_review_service

from . import ERROR_RESPONSE, Pagination

router = APIRouter()


@router.get(
    "/{accommodation_id}",
    response_model=Union[AccommodationOut, ExpandedAccommodationOut],
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation(
    accommodation_id: UUID,
    expand: Optional[bool] = False,
    accommodation_service: AccommodationService = Depends(get_accommodation_service),
    session: AsyncSession = Depends(get_async_session),
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
    pagination: Pagination = Depends(),
    accommodation_service: AccommodationService = Depends(get_accommodation_service),
    session: AsyncSession = Depends(get_async_session),
) -> list[AccommodationOut]:
    return await accommodation_service.get_accommodations(session, **pagination.model_dump())


@router.get(
    "/{accommodation_id}/reviews",
    response_model=list[ReviewOut],
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation_reviews(
    accommodation_id: UUID,
    pagination: Pagination = Depends(),
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_async_session),
) -> list[ReviewOut]:
    return await review_service.get_reviews_by_accommodation(accommodation_id, session, **pagination.model_dump())


@router.get(
    "/{accommodation_id}/reviews/{review_id}",
    response_model=ReviewOut,
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE},
)
async def get_accommodation_review(
    accommodation_id: UUID,
    review_id: UUID,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_async_session),
) -> ReviewOut:
    review = await review_service.get_review_by_accommodation(accommodation_id, review_id, session)
    if review is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Review with id={review_id} was not found in accommodation with id {accommodation_id}",
        )

    return review
