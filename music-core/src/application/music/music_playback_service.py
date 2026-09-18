from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicPlaybackService:
    def __init__(self, http_client_factory: AsyncHttpClientFactory):
        self.client_factory = http_client_factory

    async def get_status(self):
        # get status of playback service
        pass

    async def play(self, track_url: str):
        # play the track with the playback service
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
