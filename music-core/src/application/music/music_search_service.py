from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicSearchService:
    """
    Service for searching music tracks using an external search service.
    Currently we use miniDLNA for searching music tracks
    But this will be replaced with navidrome.
    """

    def __init__(self, client_factory: AsyncHttpClientFactory):
        self.client_factory = client_factory

    async def get_status(self):
        client = self.client_factory.get("dlna")

        response = await client.get("/rootDesc.xml")

        # self.client_factory.
        return response.status_code

    async def search(self, query: str) -> str:
        # search for music with the search service
        return ""
