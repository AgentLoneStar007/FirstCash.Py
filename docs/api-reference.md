# API reference

The public client is available as:

```python
from firstcash import APIClient
```

## `APIClient`

```text
APIClient(api_key: str)
```

Creates an asynchronous client for the FirstCash mobile application API.

### Parameters

- `api_key` (`str`) — API key included in every request.

The client uses a 10-second timeout. The constructor does not contact the API
or validate the key.

### `closeAsyncRequestClient`

```python
await client.closeAsyncRequestClient()
```

Closes the underlying `httpx.AsyncClient`. Call this exactly once after all
requests are complete, normally in a `finally` block.

## Categories

### `fetchCategories`

```python
categories = await client.fetchCategories()
```

Fetches the complete category list from `GET Categories`. The upstream API
describes the current hierarchy as two levels deep and returns categories in
ascending parent-ID order.

**Returns:** `list[Category]`

### `fetchTopCategories`

```python
categories = await client.fetchTopCategories()
```

Fetches categories from `GET Categories/top`. This is exposed separately
because it is a distinct upstream operation, although the upstream
documentation describes it similarly to the complete category list.

**Returns:** `list[Category]`

Use `Category.has_children` and `Category.parent_id` to inspect the returned
hierarchy. Category code `0` can be used by the geographic item search to
represent all categories.

## Items

### `searchItemsByGeoLocation`

```python
response = await client.searchItemsByGeoLocation(
    category_code,
    search_latitude,
    search_longitude,
    search_radius,
    page_index=0,
    page_size=10,
    search_term=None,
)
```

Searches `GET Items` near a coordinate. This is the simpler item-search
operation.

#### Parameters

- `category_code` (`int`) — category code from `fetchCategories()`. Use `0`
  for all categories. Accepted range: `0` through `9999`.
- `search_latitude` (`float`) — origin latitude, from `-90` through `90`.
- `search_longitude` (`float`) — origin longitude, from `-180` through `180`.
- `search_radius` (`float`) — radius in miles, from `0` through `5000`.
- `page_index` (`int`) — zero-indexed result page. Defaults to `0`.
- `page_size` (`int`) — number of results requested per page. Must be greater
  than zero and defaults to `10`.
- `search_term` (`str | None`) — optional text such as `"laptop"` or
  `"purse"`. `None` and an empty string are sent as a blank search term.

**Returns:** `StoreItemResponse`

**Validation errors:** `CategoryCodeValueError`,
`SearchCoordinateValueError`, `SearchRadiusValueError`,
`PageIndexValueError`, and `PageSizeValueError`.

If the API response contains no JSON body, the method raises
`APIContentNotFound("No items matched the query.")`. A valid JSON response
whose `results` list is empty returns a normal `StoreItemResponse` with an
empty `results` list.

### `searchItems`

```python
response = await client.searchItems(
    search_term,
    search_latitude,
    search_longitude,
    search_radius,
    search_price_high,
    search_price_low=None,
    stores=None,
    category_codes=None,
    page_index=0,
    page_size=10,
    only_clearance_items=False,
)
```

Searches `PUT Items` with store, category, price, and clearance filters.

#### Parameters

- `search_term` (`str`) — required, non-empty item description such as
  `"laptop"`.
- `search_latitude` (`float`) — origin latitude, from `-90` through `90`.
- `search_longitude` (`float`) — origin longitude, from `-180` through `180`.
- `search_radius` (`float`) — radius in miles, from `0` through `5000`.
- `search_price_high` (`float`) — non-negative maximum price.
- `search_price_low` (`float | None`) — optional non-negative minimum price.
  It cannot exceed `search_price_high`; omitted or zero is sent as `0`.
- `stores` (`list[str] | None`) — optional store numbers. Every element must
  be a numeric string representing a value from `0` through `32767`.
- `category_codes` (`list[str] | None`) — optional category codes. Every
  element must be a numeric string representing a value from `0` through
  `9999`.
- `page_index` (`int`) — zero-indexed result page. Defaults to `0`.
- `page_size` (`int`) — number of results requested per page. Must be greater
  than zero and defaults to `10`.
- `only_clearance_items` (`bool`) — when true, requests only clearance
  inventory.

**Returns:** `StoreItemResponse`

**Validation errors:** `ValueError` for a blank search term;
`SearchCoordinateValueError`, `SearchRadiusValueError`, `PriceValueError`,
`StoreIDValueError`, `CategoryCodeValueError`, `PageIndexValueError`, and
`PageSizeValueError` for invalid filters.

Store and category filters are strings in this method:

```python
response = await client.searchItems(
    search_term="laptop",
    search_latitude=39.105,
    search_longitude=-94.593,
    search_radius=50,
    search_price_low=100,
    search_price_high=800,
    stores=["1234", "5678"],
    category_codes=["100"],
)
```

Passing integer elements, such as `stores=[1234]`, is not supported because
the client validates each value with `str.isnumeric()`.

As with `searchItemsByGeoLocation()`, a non-JSON response is reported as
`APIContentNotFound`, while a valid response can contain an empty result list.

## Stores

### `searchStoresByGeoLocation`

```python
stores = await client.searchStoresByGeoLocation(
    search_latitude,
    search_longitude,
    page_index=1,
    page_size=10,
)
```

Fetches nearby stores from `GET Stores`.

#### Parameters

- `search_latitude` (`float`) — origin latitude, from `-90` through `90`.
- `search_longitude` (`float`) — origin longitude, from `-180` through `180`.
- `page_index` (`int`) — one-indexed result page. Defaults to `1`; unlike the
  item methods, page `0` is invalid.
- `page_size` (`int`) — number of results requested per page. Must be greater
  than zero and defaults to `10`.

**Returns:** `list[StoreDisplayInfo]`

The method returns an empty list when the API provides a valid empty JSON
list. A response without a JSON body raises `APIContentNotFound`.
`StoreDisplayInfo.phone` and `StoreDisplayInfo.hours` can be `None` when the
upstream data omits those fields.

**Validation errors:** `SearchCoordinateValueError`,
`PageIndexValueError`, and `PageSizeValueError`.

### `fetchStore`

```python
store = await client.fetchStore(store_id)
```

Fetches one store and its address, services, weekly opening hours, and
licenses.

#### Parameters

- `store_id` (`int`) — store number from `0` through `32767`.

**Returns:** `StoreDetails`

**Validation errors:** `StoreIDValueError`

A response without a JSON body raises
`APIContentNotFound("No store matched the provided ID.")`.

## Request errors

Network methods can also raise:

- `APIUnauthorizedError` for HTTP 403
- `APIRateLimited` for HTTP 429 and the rate-limit connection failure
  recognized by the client
- `APIServerError` for HTTP 500
- `APIResponseTimedOut` when the 10-second timeout expires
- `APIGeneralError` for other handled HTTP or connection errors

See [Exceptions](exceptions.md) for the complete hierarchy and handling
example.
