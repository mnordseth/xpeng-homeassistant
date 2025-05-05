"""Xpeng API Client."""

from __future__ import annotations

import datetime
import socket
from typing import Any

import aiohttp
import async_timeout
from aiohttp import BasicAuth

from .const import LOGGER
from .enode_models import EnodeResponse

ENODE_URL = "https://enode-api.production.enode.io"
ENODE_OAUTH_URL = "https://oauth.production.enode.io/"


class XpengApiClientError(Exception):
    """Exception to indicate a general API error."""


class XpengApiClientCommunicationError(
    XpengApiClientError,
):
    """Exception to indicate a communication error."""


class XpengApiClientAuthenticationError(
    XpengApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise XpengApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class XpengApiClient:
    """Sample API Client."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._client_id = client_id
        self._client_secret = client_secret
        self._session = session
        self._token = None
        self.vehicles = []

    async def async_get_token(self) -> Any:
        """Get oauth token."""
        LOGGER.debug("async_get_token()")
        auth = BasicAuth(self._client_id, self._client_secret)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}
        async with aiohttp.ClientSession(auth=auth) as session:
            response = await session.post(
                f"{ENODE_OAUTH_URL}/oauth2/token", data=data, headers=headers
            )

            result = await response.json()

        self._token = result["access_token"]
        self._token_expires = result["expires_in"]
        self._token_expires_at = datetime.datetime.now(
            tz=datetime.UTC
        ) + datetime.timedelta(seconds=self._token_expires)

    async def async_refresh_token(self) -> None:
        """Refresh oauth token before expiry."""
        expires_in = self._token_expires_at - datetime.datetime.now(tz=datetime.UTC)
        if expires_in < datetime.timedelta(seconds=180):
            LOGGER.debug("Refreshing token, expires in %s", expires_in)
            await self.async_get_token()

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        result = await self._api_wrapper(
            method="get",
            url=f"{ENODE_URL}/vehicles",
        )

        enode_response = EnodeResponse.from_json(result)
        self.vehicles = enode_response.data
        return self.vehicles

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        await self.async_refresh_token()
        if headers is None:
            headers = {}
        if "Authorization" in headers:
            headers.pop("Authorization")
        headers["Authorization"] = f"Bearer {self._token}"

        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise XpengApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise XpengApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise XpengApiClientError(
                msg,
            ) from exception
