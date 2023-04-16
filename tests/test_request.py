from modules.http_client import get_http_client


class TestRequest:
    """
    This test checks if our HTTP client sends request to the correct URL.

    There is no need to make the actual request - although the API used does not need any key and is free
    of charge, this always does not need to be the case. In either case, sending a real HTTP request
    over the network is slow and will cause this test to run for longer than necessary.
    All we need is a fake HTTP client that will provide us with a "response" that will make it obvious
    that we sent the right HTTP request.
    """

    def test_request_url(self):
        http_client = get_http_client()

        response = http_client.get("example.com")

        assert response.json["url"] == "example.com"
