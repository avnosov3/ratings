from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ScoreAspects(str, Enum):
    ACCESSIBILITY = "accessibility"
    ACTIVITIES = "activities"
    ADVANCED_SKI_AREA = "advancedSkiArea"
    APRES_SKI = "apresSki"
    ATMOSPHERE = "atmosphere"
    BEACH = "beach"
    CHILD_FRIENDLY = "childFriendly"
    CULTURE = "culture"
    ENTERTAINMENT = "entertainment"
    ENVIRONMENTAL = "environmental"
    FOOD = "food"
    HOUSING = "housing"
    HYGIENE = "hygiene"
    INTERIOR = "interior"
    LOCATION = "location"
    NIGHTLIFE = "nightlife"
    NOVICE_SKI_AREA = "noviceSkiArea"
    POOL = "pool"
    PRICE_QUALITY = "priceQuality"
    RESTAURANTS = "restaurants"
    ROOM = "room"
    SANITARY_STATE = "sanitaryState"
    SERVICE = "service"
    SIZE = "size"
    SURROUNDING = "surrounding"
    TERRACE = "terrace"


class ScoreFilter(BaseModel):
    score_aspect: Optional[ScoreAspects] = None


class BaseScore(BaseModel):
    id: UUID
    general_score: int
    updated_at: datetime
    score_aspects: dict


class ScoreIn(BaseScore):
    pass
