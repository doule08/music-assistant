import asyncio
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock, Mock

import pytest

from application.common.command_result import MusicCommand
from application.common.errors import TrackNotFoundError
from application.music.music_playback_service import MusicPlaybackService, PlayerStatus
from application.music.music_search_service import MusicSearchService
from application.music.music_service import MusicService
from infrastructure.http.http_client_factory import AsyncHttpClientFactory, ServerConfig


class FakeResponse:
    def __init__(self, payload=None, status_code=200):
        self._payload = payload or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def make_http_factory(client):
    return cast(AsyncHttpClientFactory, SimpleNamespace(get=lambda _name: client))


def make_mock_client() -> Any:
    return cast(Any, Mock())


def test_http_client_factory_starts_and_gets_client():
    async def scenario():
        factory = AsyncHttpClientFactory(
            {
                "wiim": ServerConfig(
                    name="wiim",
                    base_url="http://localhost:8000",
                    timeout=1,
                )
            }
        )

        await factory.start()
        client = factory.get("wiim")

        assert str(client.base_url) == "http://localhost:8000"
        assert client.timeout.connect == 1.0
        assert client.timeout.read == 1.0

        await factory.close()

    asyncio.run(scenario())


def test_http_client_factory_raises_for_unknown_client():
    factory = AsyncHttpClientFactory({})

    with pytest.raises(KeyError, match="Unknown HTTP client 'missing'"):
        factory.get("missing")


def test_http_client_factory_close_clears_clients():
    async def scenario():
        factory = AsyncHttpClientFactory(
            {
                "wiim": ServerConfig(
                    name="wiim",
                    base_url="http://localhost:8000",
                    timeout=1,
                )
            }
        )

        await factory.start()
        await factory.close()

        assert factory._clients == {}

    asyncio.run(scenario())


def test_music_search_service_get_server_status_returns_status_code():
    fake_client = make_mock_client()
    fake_client.build_request.return_value = SimpleNamespace(
        url="http://example.test/rootDesc.xml",
        headers={"Accept": "application/json"},
    )
    mock_send = AsyncMock(return_value=SimpleNamespace(status_code=204))
    fake_client.send = mock_send

    service = MusicSearchService(make_http_factory(fake_client))

    result = asyncio.run(service.get_server_status())

    assert result == 204
    mock_send.assert_awaited_once()


def test_music_search_service_get_server_status_raises_on_error():
    fake_client = make_mock_client()
    fake_client.build_request.return_value = SimpleNamespace(
        url="http://example.test/rootDesc.xml",
        headers={"Accept": "application/json"},
    )
    mock_send = AsyncMock(side_effect=RuntimeError("boom"))
    fake_client.send = mock_send

    service = MusicSearchService(make_http_factory(fake_client))

    with pytest.raises(RuntimeError, match="boom"):
        asyncio.run(service.get_server_status())


def test_music_search_service_search_returns_track_url():
    fake_client = make_mock_client()
    service = MusicSearchService(make_http_factory(fake_client))

    result = asyncio.run(service.search("queen"))

    assert result == "http://192.168.1.50:8200/MediaItems/380470.flac"


def test_music_playback_service_command_calls_http_api_correctly():
    fake_client = make_mock_client()
    mock_get = AsyncMock(return_value=FakeResponse())
    fake_client.get = mock_get
    service = MusicPlaybackService(make_http_factory(fake_client))

    asyncio.run(service._command("setPlayerCmd:pause"))

    mock_get.assert_awaited_once_with(
        "/httpapi.asp",
        params={"command": "setPlayerCmd:pause"},
    )


def test_music_playback_service_get_server_status_parses_response():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(return_value=FakeResponse({"status": "ok"}))
    service = MusicPlaybackService(make_http_factory(fake_client))

    response = asyncio.run(service.get_server_status())

    assert response == {"status": "ok"}


def test_music_playback_service_get_player_status_returns_enum():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(
        return_value=FakeResponse({"status": PlayerStatus.PLAY.value})
    )
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.get_player_status())

    assert result is PlayerStatus.PLAY


def test_music_playback_service_play_returns_true():
    fake_client = make_mock_client()
    mock_get = AsyncMock(return_value=FakeResponse())
    fake_client.get = mock_get
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.play("http://example.test/track.mp3"))

    assert result is True
    mock_get.assert_awaited_once_with(
        "/httpapi.asp",
        params={"command": "setPlayerCmd:play:http://example.test/track.mp3"},
    )


def test_music_playback_service_pause_returns_false_when_not_playing():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(
        return_value=FakeResponse({"status": PlayerStatus.PAUSE.value})
    )
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.pause())

    assert result is False
    assert fake_client.get.await_count == 1


def test_music_playback_service_pause_returns_true_when_playing():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(
        side_effect=[
            FakeResponse({"status": PlayerStatus.PLAY.value}),
            FakeResponse(),
        ]
    )
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.pause())

    assert result is True
    assert fake_client.get.await_count == 2


def test_music_playback_service_resume_returns_false_when_not_paused():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(
        return_value=FakeResponse({"status": PlayerStatus.PLAY.value})
    )
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.resume())

    assert result is False
    assert fake_client.get.await_count == 1


def test_music_playback_service_resume_returns_true_when_paused():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(
        side_effect=[
            FakeResponse({"status": PlayerStatus.PAUSE.value}),
            FakeResponse(),
        ]
    )
    service = MusicPlaybackService(make_http_factory(fake_client))

    result = asyncio.run(service.resume())

    assert result is True
    assert fake_client.get.await_count == 2


def test_music_playback_service_stop_next_previous_and_volume_return_true():
    fake_client = make_mock_client()
    fake_client.get = AsyncMock(return_value=FakeResponse())
    service = MusicPlaybackService(make_http_factory(fake_client))

    assert asyncio.run(service.stop()) is True
    assert asyncio.run(service.next()) is True
    assert asyncio.run(service.previous()) is True
    assert asyncio.run(service.set_volume(42)) is True
    assert fake_client.get.await_count == 4


def test_music_service_get_status_aggregates_server_statuses():
    service = MusicService(
        search_service=cast(
            MusicSearchService,
            SimpleNamespace(get_server_status=AsyncMock(return_value=200)),
        ),
        playback_service=cast(
            MusicPlaybackService,
            SimpleNamespace(get_server_status=AsyncMock(return_value=204)),
        ),
    )

    result = asyncio.run(service.get_status())

    assert result == {"search_status": 200, "playback_status": 204}


def test_music_service_play_returns_command_result_when_track_found():
    mock_search = AsyncMock(return_value="http://example.test/track.mp3")
    mock_play = AsyncMock(return_value=True)
    search_service = cast(
        MusicSearchService,
        SimpleNamespace(search=mock_search),
    )
    playback_service = cast(
        MusicPlaybackService,
        SimpleNamespace(play=mock_play),
    )
    service = MusicService(search_service, playback_service)

    result = asyncio.run(service.play("queen"))

    assert result.command == MusicCommand.PLAY
    assert result.success is True
    assert result.data == {"query": "queen"}
    mock_play.assert_awaited_once_with("http://example.test/track.mp3")


def test_music_service_play_raises_when_track_not_found():
    mock_search = AsyncMock(return_value="")
    mock_play = AsyncMock(return_value=True)
    search_service = cast(
        MusicSearchService,
        SimpleNamespace(search=mock_search),
    )
    playback_service = cast(
        MusicPlaybackService,
        SimpleNamespace(play=mock_play),
    )
    service = MusicService(search_service, playback_service)

    with pytest.raises(TrackNotFoundError, match="Track not found: missing"):
        asyncio.run(service.play("missing"))

    mock_play.assert_not_called()


@pytest.mark.parametrize(
    "method_name, expected_command",
    [
        ("pause", MusicCommand.PAUSE),
        ("resume", MusicCommand.RESUME),
        ("stop", MusicCommand.STOP),
        ("next", MusicCommand.NEXT),
        ("previous", MusicCommand.PREVIOUS),
    ],
)
def test_music_service_command_wrappers_return_command_result(
    method_name, expected_command
):
    playback_service = cast(
        MusicPlaybackService,
        SimpleNamespace(),
    )
    for command_name in ["pause", "resume", "stop", "next", "previous"]:
        setattr(playback_service, command_name, AsyncMock(return_value=True))

    service = MusicService(
        cast(MusicSearchService, SimpleNamespace()), playback_service
    )

    result = asyncio.run(getattr(service, method_name)())

    assert result.command == expected_command
    assert result.success is True
    assert result.data is None


def test_music_service_set_volume_returns_command_result():
    mock_set_volume = AsyncMock(return_value=True)
    playback_service = cast(
        MusicPlaybackService,
        SimpleNamespace(set_volume=mock_set_volume),
    )
    service = MusicService(
        cast(MusicSearchService, SimpleNamespace()), playback_service
    )

    result = asyncio.run(service.set_volume(55))

    assert result.command == MusicCommand.SET_VOLUME
    assert result.success is True
    assert result.data == {"volume": 55}
    mock_set_volume.assert_awaited_once_with(55)
