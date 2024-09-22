from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional

from fastapi import status
from httpx import AsyncClient, HTTPError


class StatusCodeNotOKError(Exception):
    pass


class AbstractClient(ABC):
    API_REQUEST = "ENDPOINT: {url}. HEADERS: {headers}. PARAMS: {params}. "
    API_NOT_AVALIABLE = API_REQUEST + "API not avaliable " + "ERROR: {error}."
    STATUS_CODE_ERROR = API_REQUEST + "Unexpected return code: {status_code}."

    @abstractmethod
    async def get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        pass


class CustomAsyncClient(AbstractClient):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        request_params = dict(url=url, params=params, headers=headers)
        try:
            response = await self.client.get(url=url, params=params)
        except HTTPError as error:
            message = self.API_NOT_AVALIABLE.format(**request_params, error=error)
            raise ConnectionError(message)

        response_status_code = response.status_code
        if response_status_code != status.HTTP_200_OK:
            message = self.STATUS_CODE_ERROR.format(**request_params, status_code=response_status_code)
            raise StatusCodeNotOKError(message)

        return response.json()


@lru_cache
def get_custom_client() -> CustomAsyncClient:
    return CustomAsyncClient(AsyncClient())
