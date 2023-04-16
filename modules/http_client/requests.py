import requests

from modules.http_client.base import BaseHttpClient, HttpResponse


class RequestsHttpClient(BaseHttpClient):
    def get(self, url: str) -> HttpResponse:
        response = requests.get(url)
        return HttpResponse(response.status_code, response.content)
