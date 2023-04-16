from modules.btc_api_client import get_btc_api_client


def run():
    btc_api_client = get_btc_api_client()
    btc_price_eur = btc_api_client.get_current_price_in_eur()
    return f"Current price of BTC is {btc_price_eur} EUR."


if __name__ == "__main__":
    print(run())
