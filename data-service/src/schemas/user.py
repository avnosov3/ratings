from typing import Optional

from pydantic import BaseModel, Field

from src.models.user import USER_EMAIL_LEN, USER_IPADDRES_LEN, USER_NAME_LEN


class UserIn(BaseModel):
    name: str = Field(..., alias="userName", max_length=USER_NAME_LEN)
    email: str = Field(..., alias="userEmail", max_length=USER_EMAIL_LEN)
    ip_address: Optional[str] = Field(None, alias="userIpAddress", max_length=USER_IPADDRES_LEN)
