from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicPlaybackService:
    def __init__(self, http_client_factory: AsyncHttpClientFactory):
        self.client = http_client_factory.get("wiim")

    async def get_server_status(self):
        try:
            response = await self.client.get(
                "/httpapi.asp",
                params={"command": "getStatusEx"},
            )

            return response.status_code
        except Exception as e:
            print("WIIM ERROR:", type(e).__name__, str(e))
            raise

    async def get_player_status(self):
        try:
            response = await self.client.get(
                "/httpapi.asp",
                params={"command": "getPlayerStatus"},
            )

            response.raise_for_status()

            return response.json()
        except Exception as e:
            print("WIIM ERROR:", type(e).__name__, str(e))
            raise

    async def play(self, track_url: str):

        try:
            # response = await self.client.get(
            #     "/httpapi.asp",
            #     params={"command": f"setPlayerCmd:play:{track_url}"},
            # )

            request = self.client.build_request(
                "GET",
                "/httpapi.asp",
                params={"command": f"setPlayerCmd:play:{track_url}"},
            )

            # urllib.parse.urlencode(request.url.params)
            print("REQUEST URL:", request.url)
            print("REQUEST HEADERS:", request.headers)

            response = await self.client.send(request)

            response.raise_for_status()

            print(response.json())

        except Exception as e:
            print("WIIM ERROR:", type(e).__name__, str(e))
            raise

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
