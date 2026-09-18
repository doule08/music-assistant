from infrastructure.http.http_client_factory import AsyncHttpClientFactory


class MusicSearchService:
    def __init__(self, http_client_factory: AsyncHttpClientFactory):
        self.client_factory = http_client_factory

    def get_status(self):
        # get status of search service
        pass

    def search(self, query: str):
        # search for music with the search service
        pass
