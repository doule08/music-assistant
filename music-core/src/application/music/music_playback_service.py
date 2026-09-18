from enum import Enum

from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class PlayerStatus(Enum):
    PAUSE = "pause"
    PLAY = "play"
    STOP = "stop"


class MusicPlaybackService:
    COMMANDS = {
        "server_status": "getStatusEx",
        "player_status": "getPlayerStatus",
        "pause": "setPlayerCmd:pause",
        "resume": "setPlayerCmd:resume",
        "stop": "setPlayerCmd:stop",
        "next": "setPlayerCmd:next",
        "previous": "setPlayerCmd:prev",
    }

    def __init__(self, http_client_factory: AsyncHttpClientFactory):
        self.client = http_client_factory.get("wiim")

    async def _command(self, command: str):
        try:
            response = await self.client.get(
                "/httpapi.asp",
                params={"command": command},
            )

            response.raise_for_status()

            return response

        except Exception as e:
            print("WIIM ERROR:", type(e).__name__, str(e))
            raise

    async def get_server_status(self):
        response = await self._command(self.COMMANDS["server_status"])
        return response.json()

    async def get_player_status(self) -> PlayerStatus:
        response = await self._command(self.COMMANDS["player_status"])
        return PlayerStatus(response.json()["status"])

    async def play(self, track_url: str) -> bool:
        await self._command(f"setPlayerCmd:play:{track_url}")
        return True

    async def pause(self) -> bool:
        status = await self.get_player_status()

        if status != PlayerStatus.PLAY:
            return False

        await self._command(self.COMMANDS["pause"])
        return True

    async def resume(self) -> bool:
        status = await self.get_player_status()

        if status != PlayerStatus.PAUSE:
            return False

        await self._command(self.COMMANDS["resume"])
        return True

    async def stop(self) -> bool:
        await self._command(self.COMMANDS["stop"])
        return True

    async def next(self) -> bool:
        await self._command(self.COMMANDS["next"])
        return True

    async def previous(self) -> bool:
        await self._command(self.COMMANDS["previous"])
        return True

    async def set_volume(self, volume: int) -> bool:
        await self._command(f"setPlayerCmd:vol:{volume}")
        return True
