from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicPlaybackService:
    def __init__(self, http_client_factory: AsyncHttpClientFactory):
        self.client_factory = http_client_factory

    def get_status(self):
        # get status of playback service
        pass

    def play(self, track_id: str):
        # play the track with the playback service
        pass

    def pause(self):
        # pause the playback service
        pass

    def resume(self):
        # resume the playback service
        pass

    def stop(self):
        # stop the playback service
        pass

    def next(self):
        # play the next track with the playback service
        pass

    def previous(self):
        # play the previous track with the playback service
        pass

    def set_volume(self, volume: int):
        # set the volume of the playback service
        pass
