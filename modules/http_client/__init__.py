import os

from modules.http_client.base import BaseHttpClient
from utils import import_string


def get_http_client() -> BaseHttpClient:
    return import_string(os.environ["HTTP_CLIENT_MODULE"])()
