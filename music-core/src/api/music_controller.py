from fastapi import APIRouter, Depends
from application.music.music_service import MusicService
from application.music.music_dependencies import get_music_service

router = APIRouter(tags=["Playback control"], prefix="/music")


@router.get("/status")
async def get_status(service: MusicService = Depends(get_music_service)):
    return await service.get_status()


@router.post("/play")
async def play(query: str, service: MusicService = Depends(get_music_service)):
    return await service.play(query)


@router.post("/pause")
async def pause(service: MusicService = Depends(get_music_service)):
    return await service.pause()


@router.post("/stop")
async def stop():
    return {"message": "Playback stopped"}


@router.post("/resume")
async def resume():
    return {"message": "Playback resumed"}


@router.post("/next")
async def next():
    return {"message": "Playing next track"}
