from application.music.music_playback_service import MusicPlaybackService
from application.music.music_search_service import MusicSearchService
from application.music.music_service import MusicService
from infrastructure.music.music_client_factories import (
    create_dlna_client_factory,
    create_music_playback_client_factory,
)


def get_music_service() -> MusicService:
    search_service = MusicSearchService(create_dlna_client_factory())

    playback_service = MusicPlaybackService(create_music_playback_client_factory())

    return MusicService(
        search_service,
        playback_service,
    )
