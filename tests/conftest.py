"""Shared fixtures for e2e tests against the live Watermelon API."""

import os

import pytest
import pytest_asyncio

from watermelon_mcp.client import WatermelonClient
from watermelon_mcp.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Load settings from .env (or environment)."""
    return Settings()


@pytest_asyncio.fixture
async def client(settings: Settings) -> WatermelonClient:
    """Create a live API client, close it after the test."""
    c = WatermelonClient(settings.watermelon_api_key, settings.watermelon_secret_key)
    yield c
    await c.close()
