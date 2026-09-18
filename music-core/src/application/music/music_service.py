from application.common.command_result import CommandResult, MusicCommand
from application.common.errors import TrackNotFoundError
from application.music.music_playback_service import MusicPlaybackService
from application.music.music_search_service import MusicSearchService
from infrastructure.http.http_client_factory import AsyncHttpClientFactory, ServerConfig


class MusicService:

    def __init__(
        self, search_service: MusicSearchService, playback_service: MusicPlaybackService
    ):
        self.search_service = search_service
        self.playback_service = playback_service
        pass

    async def get_status(self):
        print(" get_status service ??")
        search_status = await self.search_service.get_status()

        return search_status
        playback_status = await self.playback_service.get_status()

        return {"search_status": search_status, "playback_status": playback_status}

    async def play(self, query: str):
        track_url = await self.search_service.search(query)

        if not track_url:
            raise TrackNotFoundError(query)

        await self.playback_service.play(track_url)

        return CommandResult(
            command=MusicCommand.PLAY,
            success=True,
            data={"query": query},
        )

    async def pause(self):
        return CommandResult(
            command=MusicCommand.PAUSE,
            success=True,
        )

    async def resume(self):
        return CommandResult(
            command=MusicCommand.RESUME,
            success=True,
        )

    async def stop(self):
        return CommandResult(
            command=MusicCommand.STOP,
            success=True,
        )

    async def next(self):
        return CommandResult(
            command=MusicCommand.NEXT,
            success=True,
        )

    async def previous(self):
        return CommandResult(
            command=MusicCommand.PREVIOUS,
            success=True,
        )

    async def set_volume(self, volume: int):
        return CommandResult(
            command=MusicCommand.SET_VOLUME,
            success=True,
            data={"volume": volume},
        )
