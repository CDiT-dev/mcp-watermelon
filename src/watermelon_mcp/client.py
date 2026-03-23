"""Async HTTP client for the Watermelon.ai API."""

import logging
from typing import Any

import httpx

BASE_URL = "https://public.watermelon.ai/api/v1"

logger = logging.getLogger(__name__)


class WatermelonClient:
    """HTTP client for interacting with the Watermelon.ai public API."""

    def __init__(self, api_key: str, secret_key: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}.{secret_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
            follow_redirects=False,
        )

    async def request(self, method: str, path: str, body: Any | None = None) -> Any:
        """Make an authenticated request to the Watermelon API."""
        response = await self._client.request(
            method,
            path,
            json=body if body is not None else None,
        )

        if not response.is_success:
            logger.error(
                "Watermelon API error",
                extra={"status": response.status_code, "body": response.text, "path": path, "method": method},
            )
            if response.status_code == 429:
                raise httpx.HTTPStatusError(
                    "Rate limit exceeded (429). Retry after a moment.",
                    request=response.request,
                    response=response,
                )
            raise httpx.HTTPStatusError(
                f"Watermelon API error {response.status_code}.",
                request=response.request,
                response=response,
            )

        if response.status_code == 204:
            return None

        return response.json()

    async def get(self, path: str) -> Any:
        return await self.request("GET", path)

    async def post(self, path: str, body: Any) -> Any:
        return await self.request("POST", path, body)

    async def put(self, path: str, body: Any) -> Any:
        return await self.request("PUT", path, body)

    async def patch(self, path: str, body: Any) -> Any:
        """Partial update — use when the API endpoint supports PATCH semantics."""
        return await self.request("PATCH", path, body)

    async def delete(self, path: str) -> Any:
        return await self.request("DELETE", path)

    async def close(self) -> None:
        await self._client.aclose()
