# FirstCash.py documentation

FirstCash.py is an asynchronous Python wrapper around part of the
[FirstCash mobile application API](https://mobileapps.cashamerica.com/api/v2/).
It can fetch inventory categories, search inventory, find nearby stores, and
retrieve a store's details.

## Contents

- [Disclaimer](disclaimer.md) - **IMPORTANT!** Read this first before continuing!
- [Getting started](getting-started.md) — installation, authentication, and
  the first request
- [API reference](api-reference.md) — every supported `APIClient` method
- [Data models](models.md) — fields returned by the library
- [Exceptions](exceptions.md) — validation, network, and API errors
- [Examples](examples.md) — complete recipes for common searches

## Requirements

- Python 3.12 or newer
- A working API key

## Supported API operations

| FirstCash.py method              | Upstream operation   |
|----------------------------------|----------------------|
| `fetchCategories()`              | `GET Categories`     |
| `fetchTopCategories()`           | `GET Categories/top` |
| `searchItemsByGeoLocation(...)`  | `GET Items`          |
| `searchItems(...)`               | `PUT Items`          |
| `searchStoresByGeoLocation(...)` | `GET Stores`         |
| `fetchStore(store_id)`           | Store detail lookup  |

The upstream API also advertises users, offers, configuration, images, and
NJLC operations. FirstCash.py does not offer methods for interacting with those
endpoints either because they don't work, their behavior has not been documented
(such as the Images endpoint), or interacting with the endpoint may be destructive
to the FirstCash system (which this library tries to avoid).

## Important behavior

- All network methods are asynchronous and must be awaited.
- An `APIClient` owns an `httpx.AsyncClient`. Always call
  `closeAsyncRequestClient()` when finished to close the client.
- Item result pages are zero-indexed. Store-search pages are one-indexed.
- Search radii and returned distances are expressed in miles.
- The client has a fixed 10-second request timeout.
- Models are mutable result objects. Their fields are populated after a
  successful API response; they are not intended as request-builder classes.

## Minimal example

```python
import asyncio

from firstcash import APIClient


async def main() -> None:
    client = APIClient(api_key="<api key>")
    try:
        response = await client.searchItemsByGeoLocation(
            category_code=0,
            search_latitude=39.105,
            search_longitude=-94.593,
            search_radius=20,
        )

        for item in response.results:
            print(item)
    finally:
        await client.closeAsyncRequestClient()


asyncio.run(main())
```

See [Getting started](getting-started.md) for installation and lifecycle
details.
