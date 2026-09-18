class MusicError(Exception):
    """Base exception for music-related errors."""


class TrackNotFoundError(MusicError):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"Track not found: {query}")


class PlaybackError(MusicError):
    pass
