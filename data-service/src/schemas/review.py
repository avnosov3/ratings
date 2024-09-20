from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator
from src.models.accommodation import Accommodation
from src.models.review import (
    LOCALE_CODE_LEN,
    REVIEW_TITLE_LEN,
    REVIEW_TRAVEL_DATE_LEN,
    REVIEW_TRAVEL_PARTY_LEN,
    SOURCE_NAME_LEN,
    Locale,
    Source,
)
from src.models.user import User
from src.utils.validators import validate_timezone


class ReviewStatus(str, Enum):
    APPROVED = "approved"
    PENDING_APPROVAL = "pending_approval"
    REMOVED = "removed"


class ReviewIn(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID
    title: Optional[str] = Field(None, max_length=REVIEW_TITLE_LEN)
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    travel_date: Optional[str] = Field(None, alias="travelDate", max_length=REVIEW_TRAVEL_DATE_LEN)
    travel_party: Optional[str] = Field(None, alias="travelParty", max_length=REVIEW_TRAVEL_PARTY_LEN)
    general_score: float = Field(..., alias="generalScore")
    status: ReviewStatus
    text: str
    zoover_review_id: PositiveInt = Field(..., alias="zooverReviewId")
    score_aspects: dict
    accommodation: Accommodation
    source: Source
    locale: Locale
    user: User

    @field_validator("travel_date")
    @classmethod
    def validate_travel_date(cls, travel_date: Optional[str]):
        if travel_date is None:
            return travel_date

        for date_format in ("%Y%m", "%Y%m%d"):
            try:
                datetime.strptime(travel_date, date_format)
                return travel_date
            except ValueError:
                continue

        raise ValueError("travel date supports two formats YYYYMMDD or YYYYMM")

    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, created_at: datetime):
        return validate_timezone(created_at, "created at without timezone")

    @field_validator("updated_at")
    @classmethod
    def validate_updated_at(cls, updated_at: datetime):
        return validate_timezone(updated_at, "updated at without timezone")


class LocaleIn(BaseModel):
    code: str = Field(..., alias="locale", max_length=LOCALE_CODE_LEN)


class SourceIn(BaseModel):
    name: str = Field(..., alias="source", max_length=SOURCE_NAME_LEN)
