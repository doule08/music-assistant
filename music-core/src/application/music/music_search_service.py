from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicSearchService:
    """
    Service for searching music tracks using an external search service.
    Currently we use miniDLNA for searching music tracks
    But this will be replaced with navidrome.
    """

    def __init__(self, client_factory: AsyncHttpClientFactory):
        self.client = client_factory.get("dlna")

    async def get_status(self):
        try:
            request = self.client.build_request("GET", "/rootDesc.xml")

            print("REQUEST URL:", request.url)
            print("REQUEST HEADERS:", request.headers)

            response = await self.client.send(request)

            print("STATUS:", response.status_code)
            return response.status_code

        except Exception as e:
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR REPR:", repr(e))
            print("ERROR CAUSE:", repr(e.__cause__))
            raise

    async def search(self, query: str) -> str:
        # search for music with the search service
        return ""
