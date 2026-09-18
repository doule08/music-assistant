from application.music.music_playback_service import MusicPlaybackService
from application.music.music_search_service import MusicSearchService
from infrastructure.http.http_client_factory import AsyncHttpClientFactory, ServerConfig


class MusicService:

    # TODO : Will need two service :
    # 1 One to search the music with a mini DLNA server (later with a navidrome server)
    # 2 One to control the playback with my Wiim AMp Pro

    def __init__(
        self, search_service: MusicSearchService, playback_service: MusicPlaybackService
    ):
        self.search_service = search_service
        self.playback_service = playback_service
        pass

    # TODO
    async def get_status(self):
        # get status of search service and playback service
        pass

    async def play(self, track_id: str):
        # search for the track with the search service and play it with the playback service
        pass

    async def pause(self):
        # pause the playback service
        pass

    async def resume(self):
        # resume the playback service
        pass

    async def stop(self):
        # stop the playback service
        pass

    async def next(self):
        # play the next track with the playback service
        pass

    async def previous(self):
        # play the previous track with the playback service
        pass

    async def set_volume(self, volume: int):
        # set the volume of the playback service
        pass
