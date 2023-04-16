from modules.http_client import BaseHttpClient
from modules.http_client.base import HttpResponse


class HttpClientFake(BaseHttpClient):
    def get(self, url: str) -> HttpResponse:
        return HttpResponse(200, ('{"url": "' + url + '", "status": "ok"}').encode("utf8"))


class HttpClientStub(BaseHttpClient):
    def get(self, url: str) -> HttpResponse:
        return HttpResponse(200, '{"EUR": {"last": 15000.0}}'.encode("utf8"))
