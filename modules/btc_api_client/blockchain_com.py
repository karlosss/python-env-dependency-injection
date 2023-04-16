from modules.btc_api_client.base import BaseBtcApiClient
from modules.http_client import get_http_client


class BlockchainComClient(BaseBtcApiClient):
    API_URL = "https://blockchain.info/ticker"

    def get_current_price_in_eur(self) -> float:
        http_client = get_http_client()
        response = http_client.get(self.API_URL)
        price = response.json["EUR"]["last"]
        return float(price)
