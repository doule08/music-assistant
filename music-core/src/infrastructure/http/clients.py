from application.common.constants import (
    DLNA_URL,
    NAVIDROME_URL,
    WIIM_URL,
)

from infrastructure.http.http_client_factory import (
    AsyncHttpClientFactory,
    ServerConfig,
)


def create_http_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "dlna": ServerConfig(
                name="dlna",
                base_url=DLNA_URL,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
            "navidrome": ServerConfig(
                name="navidrome",
                base_url=NAVIDROME_URL,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
            "wiim": ServerConfig(
                name="wiim",
                base_url=WIIM_URL,
                timeout=10.0,
                headers={"Accept": "application/json"},
            ),
        }
    )
