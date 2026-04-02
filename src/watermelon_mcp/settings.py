"""Settings management using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Watermelon MCP settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    watermelon_api_key: str = Field(
        description="Watermelon.ai API key",
    )
    watermelon_secret_key: str = Field(
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

    # Keycloak auth (optional — only active when keycloak_issuer is set)
    keycloak_issuer: str = Field(
        default="",
        description="Keycloak realm issuer URL for JWT validation",
    )
    keycloak_audience: str = Field(
        default="mcp-watermelon",
        description="Expected audience claim in Keycloak-issued JWTs",
    )
    keycloak_client_id: str = Field(
        default="mcp-watermelon",
        description="Pre-registered Keycloak client ID for OIDCProxy",
    )
    keycloak_client_secret: str = Field(
        default="",
        description="Keycloak client secret for OIDCProxy",
    )
    mcp_base_url: str = Field(
        default="",
        description="Public URL of this server (for Protected Resource Metadata)",
    )
    mcp_api_key: str = Field(
        default="",
        description="Static API key for bearer token auth (Claude Code, n8n)",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get validated application settings (cached singleton)."""
    return Settings()
