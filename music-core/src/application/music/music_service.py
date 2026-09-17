from __future__ import annotations

from infrastructure.http.client_factory import AsyncHttpClientFactory, ServerConfig


def create_music_client_factory() -> AsyncHttpClientFactory:
    return AsyncHttpClientFactory(
        {
            "music-server": ServerConfig(
                name="music-server",
                base_url="http://localhost:8000",
                timeout=10.0,
                headers={"Accept": "application/json"},
            )
        }
    )


class MusicService:
    def __init__(self, client_factory: AsyncHttpClientFactory):
        self.client_factory = client_factory

    # TODO
    async def get_status(self):
        async with self.client_factory.get("music-server") as client:
            response = await client.get("/status")
            response.raise_for_status()
            return response.json()

    async def play(self, track_id: str):
        async with self.client_factory.get("music-server") as client:
            response = await client.post("/player/play", json={"track_id": track_id})
            response.raise_for_status()
            return response.json()

    async def pause(self):
        async with self.client_factory.get("music-server") as client:
            response = await client.post("/player/pause")
            response.raise_for_status()
            return response.json()
