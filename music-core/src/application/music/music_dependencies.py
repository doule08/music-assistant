from application.music.music_playback_service import MusicPlaybackService
from application.music.music_search_service import MusicSearchService
from application.music.music_service import MusicService


from fastapi import Request


def get_music_service(request: Request) -> MusicService:
    factory = request.app.state.http_client_factory

    search_service = MusicSearchService(factory)
    playback_service = MusicPlaybackService(factory)

    return MusicService(
        search_service,
        playback_service,
    )
