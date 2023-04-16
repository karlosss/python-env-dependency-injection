import os

from modules.btc_api_client.base import BaseBtcApiClient
from utils import import_string


def get_btc_api_client() -> BaseBtcApiClient:
    return import_string(os.environ["BTC_API_CLIENT_MODULE"])()
