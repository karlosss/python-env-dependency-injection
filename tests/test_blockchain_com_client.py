import pytest

from modules.btc_api_client import get_btc_api_client


@pytest.mark.env(HTTP_CLIENT_MODULE="tests.stubs.http_client.HttpClientStub")
@pytest.mark.env(BTC_API_CLIENT_MODULE="modules.btc_api_client.blockchain_com.BlockchainComClient")
class TestBtcApiClient:
    """
    This test checks if the blockchain.com client can parse the price from the response.

    The price is volatile, but we need it fixed. Therefore, we inject an HTTP client that will not do any actual
    requests, but rather provide a static response of 15000 EUR.

    To achieve this, we need to override both default variables of the test env.
    """
    def test_get_price(self):
        btc_api_client = get_btc_api_client()

        price = btc_api_client.get_current_price_in_eur()

        assert price == 15000.0
