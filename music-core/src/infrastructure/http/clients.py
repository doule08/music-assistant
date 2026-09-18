from config.settings import settings

from infrastructure.http.http_client_factory import (
    AsyncHttpClientFactory,
    ServerConfig,
)


def create_http_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "dlna": ServerConfig(
                name="dlna",
                base_url=settings.dlna_url,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
            "navidrome": ServerConfig(
                name="navidrome",
                base_url=settings.navidrome_url,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
            "wiim": ServerConfig(
                name="wiim",
                base_url=settings.wiim_url,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
        }
    )
