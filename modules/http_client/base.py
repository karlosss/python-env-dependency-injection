import json
from typing import Optional, Any


class HttpResponse:
    def __init__(self, status_code: int, body: Optional[bytes] = None):
        self.status_code = status_code
        self.body = body

    @property
    def json(self) -> dict[str, Any]:
        return json.loads(self.body)


class BaseHttpClient:
    def get(self, url: str) -> HttpResponse:
        raise NotImplementedError
