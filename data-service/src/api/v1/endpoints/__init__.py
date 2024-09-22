from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    detail: str


ERROR_RESPONSE = {"model": HTTPExceptionSchema}


class Pagination(BaseModel):
    offset: int = 0
    limit: int = 1000


PaginationDependancy = Annotated[Pagination, Depends()]
