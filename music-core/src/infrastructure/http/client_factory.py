from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

import httpx


# frozen dataclass to make it immutable and hashable, allowing it to be used as a key in dictionaries
@dataclass(frozen=True)
class ServerConfig:
    name: str
    base_url: str
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    verify_ssl: bool = True
    follow_redirects: bool = True
    default_params: dict[str, str] = field(default_factory=dict)


# class HttpClientFactory:
#     """Factory to create configured HTTP clients per backend server.

#     This pattern mirrors the .NET IHttpClientFactory approach:
#     - a single place centralizes transport configuration
#     - each backend gets its own client configuration
#     - clients are created on demand and can be scoped per use case
#     """

#     def __init__(self, servers: Mapping[str, ServerConfig] | None = None) -> None:
#         self._servers: dict[str, ServerConfig] = dict(servers or {})

#     def register(self, name: str, config: ServerConfig) -> None:
#         self._servers[name] = config

#     def get(self, name: str) -> httpx.Client:
#         if name not in self._servers:
#             raise KeyError(
#                 f"Unknown server '{name}'. Available: {sorted(self._servers)}"
#             )

#         config = self._servers[name]

#         return httpx.Client(
#             base_url=self._normalize_base_url(config.base_url),
#             timeout=config.timeout,
#             headers=httpx.Headers(config.headers),
#             verify=config.verify_ssl,
#             follow_redirects=config.follow_redirects,
#         )

#     @staticmethod
#     def _normalize_base_url(base_url: str) -> str:
#         cleaned = base_url.rstrip("/")
#         return f"{cleaned}/"


class AsyncHttpClientFactory:
    """Async variant for FastAPI / async endpoints."""

    def __init__(self, servers: Mapping[str, ServerConfig] | None = None) -> None:
        self._servers: dict[str, ServerConfig] = dict(servers or {})

    # Register a new server configuration
    def register(self, name: str, config: ServerConfig) -> None:
        self._servers[name] = config

    # Get an async client for a given server name
    def get(self, name: str) -> httpx.AsyncClient:
        if name not in self._servers:
            raise KeyError(
                f"Unknown server '{name}'. Available: {sorted(self._servers)}"
            )

        config = self._servers[name]

        return httpx.AsyncClient(
            base_url=self._normalize_base_url(config.base_url),
            timeout=config.timeout,
            headers=httpx.Headers(config.headers),
            verify=config.verify_ssl,
            follow_redirects=config.follow_redirects,
        )

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        cleaned = base_url.rstrip("/")
        return f"{cleaned}/"
