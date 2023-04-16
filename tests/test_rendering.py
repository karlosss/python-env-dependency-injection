from main import run


class TestRendering:
    """
    Test if the string gets rendered correctly.

    The actual bitcoin price is irrelevant for this test, plus it changes over time, which would
    make this test flaky. Therefore, we replace the API by a stub that always returns the
    price of BTC as 20000 EUR, which perfectly serves the purpose of this test.
    """
    def test_string_format(self):
        output = run()

        assert output == "Current price of BTC is 20000.0 EUR."
