# Dependency injection in Python using environment variables

This is a sample project of how dependency injection can be implemented using
environment variables.

## The project

The project is very simple - retrieves the price of 
Bitcoin using an API and prints it. Also contains tests.

We would like to test three things:
- Check if the HTTP client makes a request to the right URL
- Check if the project can parse the price of Bitcoin from the API response
- Check if the output of the program gets rendered correctly

## "Simple" approach

The simple approach to implement such a program would be something like this:

```python
import requests

API_URL = "https://blockchain.info/ticker"

def main():
    response = requests.get(API_URL)
    btc_price = response.json()["EUR"]["last"]
    return f"The current price of BTC in EUR is {btc_price}"
```

## Issues of the simple approach

First issue we will encounter is while testing: the volatility in the price
of Bitcoin will cause our tests to fail:

```python
def test_output():
    assert main() == "The current price of BTC in EUR is 20000"
```

From the testcase code, it should be obvious that it will fail as soon as the
price of Bitcoin changes from exactly 20 000 EUR.

### Mocking

The most straightforward way to patch the test is to use mocks in pytest:
```python
def test_output(mocker):
    mocker.patch("main.requests.Response.json", return_value={"EUR": {"last": 20000}})
    assert main() == "The current price of BTC in EUR is 20000"
```

Now, the test will pass. Is it the best solution? Not at all: we are still
sending the actual request, which might be a waste of money in case the API
is paid, otherwise it is "just" waste of time during the test run. We improve
the solution and mock the actual request:

```python
import requests

def test_output(mocker):
    mocker.patch("main.requests.get", return_value=requests.Response(...))
    assert main() == "The current price of BTC in EUR is 20000"
```

At this point, this code is getting pretty complicated: we need to create a `requests.Response`-like object
and initialize the response content so that it will look like it was an actual response so that `.json()`
will actually work on it. Regardless of if we use the actual `requests.Response` or just create a plain
object that will just have a `.json()` method on it, we are staring to hack a bit too much:
- At this point, our dummy object construction is more complex than the original code, meaning errors
are more likely in the test than in the actual app; the more complex the interface becomes, the more awkward will
the monkeypatching be (property, class property, ...)
- Even when we mock (monkey-patch) successfully, we are using the app in a way it will never be used on production
so the behavior is not too well resembled
- If we forget to mock (monkey-patch) something in tests, it will default to production settings,
which is dangerous (loss of money on paid apis, leak of production data, ...)
- The way mocking works in `pytest` is fragile - upon moving something, the string path is no longer valid
(it is just a string, so IDEs can potentially struggle)
- Mocks, in the theory of software engineering, are dummy objects served for tracking calls. Here, we exploit
those to override some lines of code in tests

### Coupling

Our app has more issues than that, all of them having a common factor: tight coupling.
More specifically, both `requests` library and `blockchain.info` are tightly wired in
our application. Luckily, our application is small enough That brings the following issues:
- If a critical bug is discovered in `requests` or the library becomes no longer maintained, we
will need to replace it. In our case, it will mean to go over the whole codebase and rewrite
all calls to it that can be arbitrarily scattered. If we even manage to do it correctly, it will
take a lot of time.
- If we want to change the source of data from `blockchain.info` to something else, a similar story
will happen - we will need to go over the whole codebase and remove all notions of it.
- Although the output rendering does not require real data, we need them to be able
to implement the output rendering. That creates a dependency, meaning we need to
code the whole API parsing part before the work on output rendering can start.
Not a problem in such a small project, but if we had a separate developer (or even team)
working on each of the parts, one would need to wait for the other to finish their job first.
- As the application grows and the logic becomes more complex, everything being coupled together
will make everything much harder to understand, extend, maintain. Scaling will only be possible vertically
without any rewrites.

## Dependency Inversion Principle

Dependency Inversion Principle (DIP) is one of the five SOLID principles in software engineering.
It offers a solution to the problems described above and the definition is pretty simple:
```
Classes should depend on abstractions, not on concretions.
```
Let's specify what it means for our app:
- Output rendering does not need to know which service is used to get the price data.
- The API client does not need to know which specific HTTP library it uses.

### Why not to have powerful components being able to access everything?

The answer is simple: complexity. Imagine going to a restaurant. You order a meal,
you eventually get the meal you ordered. The cooking process is abstracted from you:
can you see it? Maybe yes, if you ask nicely. Do you need to understand it 
to be able to enjoy your food? It makes your life much easier that you can
eat a meal without needing to understand how to cook it.

Now replace the roles in the story above: the cook is you, the customer is a developer
in a different team than wants to use your stuff, and you are no longer cooking, but
rather coding. Let's not force the poor guy to understand all the internals of
your component, just familiarize them with the public interface and abstract the
rest away.

### Dependency Inversion vs. Dependency Injection

Now that we share the public interface on our component instead of the actual component,
we will need some mechanism to choose the actual implementation of the component and
provide it at runtime. This is called dependency injection: the actual component is 'injected'
to the interface.

### Components vs. different environments

To perform the injection, we need to know which components to inject. This configuration
can be different for each environment, including the test one.

### Components for testing

This offers an interesting opportunity: for tests, we can have an HTTP client that makes
no actual requests and provides a static response. In software engineering, this is called a stub.
On production, we will ask `blockchain.info` what the price of Bitcion is. In tests, the price
of Bitcion in just 20 000 EUR. To test the rendering, the stub will do just fine.

## Example

Let's use BTC API client as an example.

### The interface

The interface is simple: just retrieve the price of Bitcion in EUR.

```python
class BaseBtcApiClient:
    def get_current_price_in_eur(self) -> float:
        raise NotImplementedError
```

### The implementations

We have two implementations: one for tests, and one for production.

Production:

```python
from modules.btc_api_client.base import BaseBtcApiClient
from modules.http_client import get_http_client


class BlockchainComClient(BaseBtcApiClient):
    API_URL = "https://blockchain.info/ticker"

    def get_current_price_in_eur(self) -> float:
        http_client = get_http_client()
        response = http_client.get(self.API_URL)
        price = response.json["EUR"]["last"]
        return float(price)
```

Test:

```python
from modules.btc_api_client.base import BaseBtcApiClient


class BtcApiClientStub(BaseBtcApiClient):
    def get_current_price_in_eur(self) -> float:
        return 20_000.0
```

The production component needs an HTTP API client, while the test does not need one.

### The injection

There are frameworks in Python to achieve dependency injection. The solution offered
in this project is very lightweight: imports the component whose path is specified
in the respective environment variable. For each environment, a different configuration
can exist. In case a testcase needs to use some other component than the rest of the tests
(maybe that one testcase that checks if the actual external API still works), this variable
can easily be overriden using [pytest-override-env-var](https://github.com/karlosss/pytest-override-env-var)
module.

The actual injection looks like this:
```python
import os

from modules.btc_api_client.base import BaseBtcApiClient
from utils import import_string


def get_btc_api_client() -> BaseBtcApiClient:
    return import_string(os.environ["BTC_API_CLIENT_MODULE"])()
```

and to get the actual component, just store the return value of the function:
```python
btc_api_client = get_btc_api_client()
```

