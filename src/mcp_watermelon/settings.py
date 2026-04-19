"""Settings management using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Watermelon MCP settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    watermelon_api_key: SecretStr = Field(
        description="Watermelon.ai API key",
    )
    watermelon_secret_key: SecretStr = Field(
        description="Watermelon.ai secret key",
    )

    mcp_transport: Literal["stdio", "streamable-http"] = Field(
        default="stdio",
        description="MCP transport: 'stdio' for local, 'streamable-http' for container deployment",
    )
    mcp_host: str = Field(
        default="127.0.0.1",
        description="Host to bind to (use 0.0.0.0 in containers)",
    )
    mcp_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Port for streamable-http transport",
    )

    mcp_api_key: SecretStr = Field(
        default=SecretStr(""),
        description="Static API key for bearer token auth (Claude Code, n8n)",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get validated application settings (cached singleton)."""
    return Settings()
