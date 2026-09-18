import httpx

from infrastructure.http.http_client_factory import AsyncHttpClientFactory, ServerConfig


def test_factory_returns_configured_httpx_client():
    factory = AsyncHttpClientFactory(
        {
            "music-api": ServerConfig(
                name="music-api",
                base_url="https://api.example.com",
                timeout=5.0,
                headers={"X-Api-Key": "secret"},
            )
        }
    )

    client = factory.get("music-api")

    assert isinstance(client, httpx.Client)
    assert str(client.base_url) == "https://api.example.com/"
    assert client.timeout.connect == 5.0
    assert client.timeout.read == 5.0
    assert client.timeout.write == 5.0
    assert client.timeout.pool == 5.0
    assert client.headers.get("X-Api-Key") == "secret"

    client.close()


def test_factory_raises_when_server_is_unknown():
    factory = AsyncHttpClientFactory()

    try:
        factory.get("missing-server")
        assert False, "Expected KeyError to be raised"
    except KeyError:
        pass
