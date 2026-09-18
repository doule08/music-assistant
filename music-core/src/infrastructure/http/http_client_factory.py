from dataclasses import dataclass, field
from typing import Mapping

import httpx


@dataclass(frozen=True)
class ServerConfig:
    name: str
    base_url: str
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    verify_ssl: bool = True
    follow_redirects: bool = True
    default_params: dict[str, str] = field(default_factory=dict)


class AsyncHttpClientFactory:

    def __init__(self, servers: Mapping[str, ServerConfig]) -> None:
        self._servers = dict(servers)
        self._clients: dict[str, httpx.AsyncClient] = {}

    async def start(self) -> None:
        for name, config in self._servers.items():
            self._clients[name] = httpx.AsyncClient(
                base_url=self._normalize_base_url(config.base_url),
                timeout=config.timeout,
                headers=httpx.Headers(config.headers),
                verify=config.verify_ssl,
                follow_redirects=config.follow_redirects,
                params=config.default_params,
            )

    def get(self, name: str) -> httpx.AsyncClient:
        if name not in self._clients:
            raise KeyError(
                f"Unknown HTTP client '{name}'. " f"Available: {sorted(self._clients)}"
            )

        return self._clients[name]

    async def close(self) -> None:
        await self._close_clients()

    async def _close_clients(self) -> None:
        clients = list(self._clients.values())
        self._clients.clear()

        for client in clients:
            await client.aclose()

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        return f"{base_url.rstrip('/')}/"
