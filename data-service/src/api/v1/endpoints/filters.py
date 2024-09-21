from typing import Optional

from pydantic import BaseModel
from src.repositories.review import TimeFrame
from src.schemas.review import ReviewStatus


class AccommodationFilters(BaseModel):
    status: Optional[ReviewStatus] = None
    time_frame: Optional[TimeFrame] = None
