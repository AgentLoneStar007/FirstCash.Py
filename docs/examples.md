# Examples

Each example assumes an authorized API key is stored in the `FIRSTCASH_API_KEY` environment variable.

## List categories

```python
import asyncio
import os

from firstcash import APIClient


async def main() -> None:
    client = APIClient(os.environ["FIRSTCASH_API_KEY"])
    try:
        categories = await client.fetchCategories()

        for category in categories:
            relationship = (
                f"child of {category.parent_id}"
                if category.parent_id is not None
                else "top level"
            )
            print(
                category.category_code,
                category.category_name,
                relationship,
            )
    finally:
        await client.closeAsyncRequestClient()


asyncio.run(main())
```

Use a returned `category_code` in an item search. The geographic item search
also accepts `0` for all categories.

## Search items near a location

```python
import asyncio
import os

from firstcash import APIClient


async def main() -> None:
    client = APIClient(os.environ["FIRSTCASH_API_KEY"])
    try:
        response = await client.searchItemsByGeoLocation(
            category_code=0,
            search_latitude=39.105,
            search_longitude=-94.593,
            search_radius=20,
            search_term="laptop",
            page_index=0,
            page_size=25
        )

        print(
            f"Showing {len(response.results)} of "
            f"{response.number_items_total} matching items"
        )

        for item in response.results:
            print(
                f"{item.item_name}: ${item.price:.2f} "
                f"at store {item.store_number} "
                f"({item.distance:.1f} miles away)"
            )
    finally:
        await client.closeAsyncRequestClient()


asyncio.run(main())
```

## Search with store, category, and price filters

The `stores` and `category_codes` arguments require lists of numeric strings,
not integers.

```python
response = await client.searchItems(
    search_term="laptop",
    # Around-ish Lake Worth, TX
    search_latitude=32.80981572425931,
    search_longitude=-97.44110003738022,
    search_radius=50,
    search_price_low=100,
    search_price_high=800,
    # Cash America locations in Azle, Saginaw, and Lake Worth, Texas.
    stores=["2108", "2355", "2117"],
    category_codes=["100", "200"],
    page_index=0,
    page_size=25,
    only_clearance_items=False
)

for item in response.results:
    clearance = " (clearance)" if item.is_clearance_item else ""
    print(f"{item.long_icn}: {item.item_name} — ${item.price:.2f}{clearance}")
```

To leave a filter unrestricted, omit it or pass `None`:

```python
response = await client.searchItems(
    search_term="purse",
    search_latitude=39.105,
    search_longitude=-94.593,
    search_radius=50,
    search_price_high=500,
    stores=None,
    category_codes=None
)
```

## Find nearby stores

Store-search pages start at `1`.

```python
stores = await client.searchStoresByGeoLocation(
    search_latitude=39.105,
    search_longitude=-94.593,
    page_index=1,
    page_size=20
)

for store in stores:
    status = (
        store.hours.store_status
        if store.hours is not None
        else "hours unavailable"
    )
    phone = store.phone or "phone unavailable"
    print(
        f"{store.brand} {store.store_number}\n"
        f"  {store.address}\n"
        f"  {store.distance:.1f} miles — {status} — {phone}"
    )
```

## Fetch full store details

Pass the store number as an integer to `fetchStore()`:

```python
store = await client.fetchStore(store_id=1234)

print(store.short_name, store.phone)
print(store.address)

print("Services:")
for service in store.services:
    print(f"- {service}")

print("Weekly hours:")
for hours in store.weekly_hours:
    today = " (today)" if hours.is_today else ""
    print(f"- {hours.weekday}: {hours.open_time}–{hours.close_time}{today}")

if store.licenses:
    print("Licenses:")
    for license_info in store.licenses:
        print(
            f"- {license_info.license_type}: "
            f"{license_info.license_number}"
        )
```

Nearby-store results expose `store_number` as a string, so convert it before a
detail lookup:

```python
nearby = await client.searchStoresByGeoLocation(
    search_latitude=39.105,
    search_longitude=-94.593,
)

if nearby:
    details = await client.fetchStore(int(nearby[0].store_number))
    print(details)
```

## Fetch every item page

Item pages are zero-indexed. The response reports the total page count:

```python
from firstcash import StoreItem


async def search_all_pages(
    client: APIClient,
    *,
    category_code: int,
    latitude: float,
    longitude: float,
    radius: float,
) -> list[StoreItem]:
    first_page = await client.searchItemsByGeoLocation(
        category_code=category_code,
        search_latitude=latitude,
        search_longitude=longitude,
        search_radius=radius,
        page_index=0,
        page_size=50
    )

    items = list(first_page.results)
    for page_index in range(1, first_page.number_pages_total):
        page = await client.searchItemsByGeoLocation(
            category_code=category_code,
            search_latitude=latitude,
            search_longitude=longitude,
            search_radius=radius,
            page_index=page_index,
            page_size=50
        )
        items.extend(page.results)

    return items
```

The API may change between page requests. If a stable snapshot matters, the
application should account for items being added, removed, or reordered while
pagination is in progress.
