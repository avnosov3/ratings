from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from src.models.accommodation import (
    ACCOMMODATION_EMAIL_LEN,
    ACCOMMODATION_NAME_LEN,
    ACCOMMODATION_PHONE_LEN,
    ACCOMMODATION_SLUG_LEN,
    ACCOMMODATION_STREET_LEN,
    ACCOMMODATION_TYPE_LEN,
    ACCOMMODATION_URL_LEN,
    ACCOMMODATION_ZIP_CODE_LEN,
    AMENITY_NAME_LEN,
    FILE_TITLE_LEN,
    Accommodation,
)


class AccommodationIn(BaseModel):
    id: UUID
    type: str = Field(..., alias="accommodationType", max_length=ACCOMMODATION_TYPE_LEN)
    name: str = Field(..., max_length=ACCOMMODATION_NAME_LEN)
    created_at: datetime = Field(..., alias="_createdAt")
    updated_at: datetime = Field(..., alias="_updatedAt")
    slug: str = Field(..., max_length=ACCOMMODATION_SLUG_LEN)
    stars: PositiveInt
    zip_code: str = Field(..., max_length=ACCOMMODATION_ZIP_CODE_LEN)
    street: str = Field(..., max_length=ACCOMMODATION_STREET_LEN)
    phone: str = Field(..., max_length=ACCOMMODATION_PHONE_LEN)
    email: str = Field(..., max_length=ACCOMMODATION_EMAIL_LEN)
    url: str = Field(..., max_length=ACCOMMODATION_URL_LEN)
    is_bookable: bool = Field(..., alias="isBookable")
    latitude: float
    longitude: float
    zoover_gold_award: bool = Field(..., alias="zooverGoldAward")
    zoover_silver_award: bool = Field(..., alias="zooverSilverAward")
    default_price: PositiveInt = Field(..., alias="defaultPrice")
    facts: list[dict]

    @classmethod
    def build(cls, data: dict) -> "AccommodationIn":
        return cls(
            **data,
            zip_code=data["address"]["zipcode"],
            street=data["address"]["street"],
            phone=data["contactInformation"]["phone"],
            email=data["contactInformation"]["email"],
            url=data["contactInformation"]["url"],
            latitude=data["geo"]["coordinates"][1],
            longitude=data["geo"]["coordinates"][0],
        )


class AccommodationOut(BaseModel):
    id: UUID
    type: str
    name: str
    created_at: datetime
    updated_at: datetime
    slug: str
    stars: int
    zip_code: str
    street: str
    phone: str
    email: str
    is_bookable: bool
    latitude: float
    longitude: float
    zoover_gold_award: bool
    zoover_silver_award: bool
    default_price: int
    facts: list[dict]


class ExpandedAccommodationOut(AccommodationOut):
    files: list["FileOut"]
    amenities: list["AmenityOut"]


class FileIn(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    source_url: str = Field(..., alias="sourceUrl")
    rotation_degrees: Optional[bool] = Field(None, alias="rotationDegrees")
    title: str = Field(..., max_length=FILE_TITLE_LEN)
    is_top: bool = True
    is_default: bool
    accommodation: Accommodation


class FileOut(BaseModel):
    id: UUID
    title: str
    source_url: str
    is_top: bool = True
    is_default: bool


class AmenityIn(BaseModel):
    name: str = Field(..., max_length=AMENITY_NAME_LEN)


class AmenityOut(AmenityIn):
    name: str
