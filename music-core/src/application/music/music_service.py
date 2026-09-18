from application.common.command_result import CommandResult, MusicCommand
from application.common.errors import TrackNotFoundError
from application.music.music_playback_service import MusicPlaybackService
from application.music.music_search_service import MusicSearchService


class MusicService:

    def __init__(
        self, search_service: MusicSearchService, playback_service: MusicPlaybackService
    ):
        self.search_service = search_service
        self.playback_service = playback_service
        pass

    async def get_status(self):
        search_server_status_code = await self.search_service.get_server_status()
        playback_server_status_code = await self.playback_service.get_server_status()

        return {
            "search_status": search_server_status_code,
            "playback_status": playback_server_status_code,
        }

    async def play(self, query: str):
        track_url = await self.search_service.search(query)

        if not track_url:
            raise TrackNotFoundError(query)

        success = await self.playback_service.play(track_url)

        return CommandResult(
            command=MusicCommand.PLAY,
            success=success,
            data={"query": query},
        )

    async def pause(self):
        success = await self.playback_service.pause()
        return CommandResult(
            command=MusicCommand.PAUSE,
            success=success,
        )

    async def resume(self):
        success = await self.playback_service.resume()
        return CommandResult(
            command=MusicCommand.RESUME,
            success=success,
        )

    async def stop(self):
        success = await self.playback_service.stop()
        return CommandResult(
            command=MusicCommand.STOP,
            success=success,
        )

    async def next(self):
        success = await self.playback_service.next()
        return CommandResult(
            command=MusicCommand.NEXT,
            success=success,
        )

    async def previous(self):
        success = await self.playback_service.previous()
        return CommandResult(
            command=MusicCommand.PREVIOUS,
            success=success,
        )

    async def set_volume(self, volume: int):
        success = await self.playback_service.set_volume(volume)
        return CommandResult(
            command=MusicCommand.SET_VOLUME,
            success=success,
            data={"volume": volume},
        )
