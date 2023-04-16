class BaseBtcApiClient:
    def get_current_price_in_eur(self) -> float:
        raise NotImplementedError
