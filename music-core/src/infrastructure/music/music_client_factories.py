from infrastructure.http.http_client_factory import AsyncHttpClientFactory, ServerConfig


def create_dlna_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "dlna-server": ServerConfig(
                name="dlna-server",
                base_url="http://localhost:8200",
                timeout=10.0,
                headers={"Accept": "application/json"},
            )
        }
    )


def create_navidrome_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "navidrome": ServerConfig(
                name="navidrome-server",
                base_url="http://localhost:4533",
                timeout=10.0,
                headers={"Accept": "application/json"},
            )
        }
    )


def create_music_playback_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "wiim-server": ServerConfig(
                name="wiim-server",
                base_url="http://localhost:8080",
                timeout=10.0,
                headers={"Accept": "application/json"},
            )
        }
    )
