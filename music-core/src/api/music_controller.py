from typing import Annotated
from fastapi import APIRouter, Depends, Query
from application.music.music_service import MusicService
from application.music.music_dependencies import get_music_service

router = APIRouter(tags=["Playback control"], prefix="/music")


@router.get("/status")
async def get_status(service: MusicService = Depends(get_music_service)):
    return await service.get_status()


@router.post("/play")
async def play(
    query: str | None = None, service: MusicService = Depends(get_music_service)
):
    query = "TEMP EMPTY QUERY"
    return await service.play(query)


@router.post("/pause")
async def pause(service: MusicService = Depends(get_music_service)):
    return await service.pause()


@router.post("/stop")
async def stop(service: MusicService = Depends(get_music_service)):
    return await service.stop()


@router.post("/resume")
async def resume(service: MusicService = Depends(get_music_service)):
    return await service.resume()


@router.post("/next")
async def next(service: MusicService = Depends(get_music_service)):
    return await service.next()


@router.post("/volume")
async def set_volume(
    volume: Annotated[
        int, Query(ge=0, le=100, description="Volume level from 0 to 100")
    ],
    service: MusicService = Depends(get_music_service),
):
    return await service.set_volume(volume)
