from typing import Annotated, Optional

from fastapi import Depends
from pydantic import BaseModel
from src.repositories.review import TimeFrame
from src.schemas.review import ReviewStatus


class AccommodationFilters(BaseModel):
    status: Optional[ReviewStatus] = None
    time_frame: Optional[TimeFrame] = None


AccommodationFiltersDependency = Annotated[AccommodationFilters, Depends()]
