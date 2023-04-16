from modules.btc_api_client.base import BaseBtcApiClient


class BtcApiClientStub(BaseBtcApiClient):
    def get_current_price_in_eur(self) -> float:
        return 20_000.0
