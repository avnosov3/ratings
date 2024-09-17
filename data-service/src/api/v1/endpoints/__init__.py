from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    detail: str


ERROR_RESPONSE = {"model": HTTPExceptionSchema}
