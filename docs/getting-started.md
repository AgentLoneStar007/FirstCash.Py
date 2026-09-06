# Getting started

## Installation

FirstCash.py requires Python 3.12 or newer.

With pip:

```bash
python -m pip install -U firstcash.py
```

With uv:

```bash
uv add firstcash.py
```

## API key

Create the client with a FirstCash API key that you are authorized to use:

```python
from firstcash import APIClient

client = APIClient(api_key="<api key>")
```

**NOTE:** FirstCash reads the key from the URL request rather than appending it to the headers like most
other APIs. This library cleans the key from errors, but anyone using this library should do their upmost
to avoid logging connections, or by trying to scrub the key from logs. HTTPX is used to make requests in
the client, so tampering with its logging handler may be required. More research is required here.

For best practice, place your key in an environment (`.env`) file. Example:
```dotenv
FIRSTCASH_API_KEY="supercalifragilisticexpialidocius (did not google that so that's crazy if it's spelt right"
```
Then you can read the key using `os.getenv()`:
```python
import os
from firstcash import APIClient

API_KEY: str | None = os.getenv("FIRSTCASH_API_KEY")

client = APIClient(api_key=API_KEY)
```
The `python_dotenv` package is recommended to load variables from a dotenv file. Install it, then load
the file using,
```python
import os
from dotenv import load_dotenv
# Load the .env file's variables
load_dotenv()
# Then grab the key
API_KEY: str | None = os.getenv("FIRSTCASH_API_KEY")
```

## Client lifecycle

Every `APIClient` creates an internal asynchronous HTTP client with a
10-second timeout. Close it after the final request, including when a request
raises an exception:

```python
import asyncio
import os

from firstcash import APIClient


async def main() -> None:
    client = APIClient(api_key=os.environ["FIRSTCASH_API_KEY"])
    try:
        categories = await client.fetchCategories()
        for category in categories:
            print(category.category_code, category.category_name)
    finally:
        await client.closeAsyncRequestClient()


asyncio.run(main())
```

`APIClient` does not currently implement an asynchronous context manager, so
`async with APIClient(...)` is not supported.

## Your first item search

Use category code `0` to search all categories:

```python
response = await client.searchItemsByGeoLocation(
    category_code=0,
    search_latitude=39.105,
    search_longitude=-94.593,
    search_radius=20
)

print(
    f"{response.number_items_total} matches "
    f"across {response.number_pages_total} pages"
)

for item in response.results:
    print(item.item_name, item.price, item.store_number)
```

This method returns a `StoreItemResponse`; its `results` field contains
`StoreItem` objects.

## Pagination conventions

The upstream operations do not use one consistent starting index:

- `searchItemsByGeoLocation()` and `searchItems()` start at page `0`.
- `searchStoresByGeoLocation()` starts at page `1`.

Passing page `0` to `searchStoresByGeoLocation()` raises
`PageIndexValueError`.

## Input limits

FirstCash.py checks the following values before making a request:

| Input            | Accepted values                             |
|------------------|---------------------------------------------|
| Latitude         | `-90` through `90`                          |
| Longitude        | `-180` through `180`                        |
| Search radius    | `0` through `5000` miles                    |
| Store ID         | `0` through `32767`                         |
| Category code    | `0` through `9999`                          |
| Item page index  | `0` or greater                              |
| Store page index | `1` or greater                              |
| Page size        | `1` or greater                              |
| Price filters    | Non-negative; minimum cannot exceed maximum |

See [Exceptions](exceptions.md) for the errors raised by failed validation and
API requests.
