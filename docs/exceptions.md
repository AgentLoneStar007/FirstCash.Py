# Exceptions

All library-specific exceptions are importable from `firstcash`.

```python
from firstcash import FirstCashException
```

`FirstCashException` is the base class for API and validation errors defined
by the package. A blank search term passed to `searchItems()` is the one
validation case that raises Python's built-in `ValueError` instead.

## API and network exceptions

| Exception              | Meaning                                                           |
|------------------------|-------------------------------------------------------------------|
| `APIUnauthorizedError` | The API returned HTTP 403. Check the API key and endpoint access. |
| `APIRateLimited`       | The API rate-limited the connection.                              |
| `APIServerError`       | The API returned HTTP 500.                                        |
| `APIResponseTimedOut`  | A request exceeded the client's 10-second timeout.                |
| `APIContentNotFound`   | A search or store lookup received a response with no JSON body.   |
| `APIGeneralError`      | Another handled HTTP-status or connection error occurred.         |

**Notes**:

`APIRateLimited` is handled hackishly because the API does not correctly return
HTTP code 429. It should still be raised when rate-limited, though.

`APIContentNotFound` does not map directly to HTTP 404. The current client
uses it when decoding an empty or otherwise non-JSON response fails. A normal
JSON response containing an empty list is returned normally.

Currently, the library does not handle malformed data. This is planned in the future, but currently
methods may raise `KeyError` if for some reason the API fails. But this should never happen. FirstCash
does not update their systems or schemas, trust me.

## Validation exceptions

| Exception                    | Raised when                                                                          |
|------------------------------|--------------------------------------------------------------------------------------|
| `SearchCoordinateValueError` | Latitude is outside `-90...90`, or longitude is outside `-180...180`.                |
| `SearchRadiusValueError`     | Radius is outside `0...5000` miles.                                                  |
| `StoreIDValueError`          | A store ID is outside `0...32767`, or a store filter is not a numeric string.        |
| `CategoryCodeValueError`     | A category code is outside `0...9999`, or a category filter is not a numeric string. |
| `PageIndexValueError`        | An item page is below `0`, or a store page is below `1`.                             |
| `PageSizeValueError`         | Page size is less than `1`.                                                          |
| `PriceValueError`            | A price is negative, or minimum price exceeds maximum price.                         |
| `ValueError`                 | `searchItems()` receives a blank search term.                                        |

## Handling errors

Catch narrow exceptions when the application can respond differently to
specific failures, then use `FirstCashException` as a fallback:

```python
from firstcash import (
    APIContentNotFound,
    APIRateLimited,
    APIUnauthorizedError,
    FirstCashException,
)

try:
    response = await client.searchItemsByGeoLocation(
        category_code=0,
        search_latitude=39.105,
        search_longitude=-94.593,
        search_radius=20,
    )
except APIUnauthorizedError:
    print("The API key is invalid!")
except APIRateLimited:
    print("The request was rate-limited.")
except APIContentNotFound:
    print("No matching response content was returned.")
except FirstCashException as error:
    print(f"API request failed: {error}")
```

For `searchItems()`, catch `ValueError` separately if a blank search term can
come from user input:

```python
try:
    response = await client.searchItems(
        search_term=user_search_term,
        search_latitude=39.105,
        search_longitude=-94.593,
        search_radius=20,
        search_price_high=500,
    )
except ValueError as error:
    print(error)
except FirstCashException as error:
    print(f"API request failed: {error}")
```
