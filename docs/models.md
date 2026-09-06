# Data models

The response models are available directly from `firstcash`:

```python
from firstcash import (
    Category,
    StoreAddress,
    StoreDetails,
    StoreDisplayInfo,
    StoreHours,
    StoreItem,
    StoreItemResponse,
    StoreLicense,
    TodaysStoreHours,
)
```

These are mutable result containers. They declare their fields with type
annotations, but most do not define constructors that accept field values.
Normally, obtain populated instances from an `APIClient` method rather than
constructing them yourself.

## `Category`

Returned by `fetchCategories()` and `fetchTopCategories()`.

| Field           | Type          | Description                                     |
|-----------------|---------------|-------------------------------------------------|
| `category_code` | `str`         | Category code used by item searches.            |
| `category_name` | `str`         | Human-readable category name.                   |
| `parent_id`     | `str \| None` | Parent category ID, or `None` when absent.      |
| `has_children`  | `bool`        | Whether the category contains child categories. |

`str(category)` and `repr(category)` produce
`"<category name> (<category code>)"`.

## `StoreItemResponse`

Returned by both item-search methods.

| Field | Type | Description |
| --- | --- | --- |
| `results` | `list[StoreItem]` | Items on the requested page. |
| `number_pages_total` | `int` | Total matching result pages. |
| `number_items_total` | `int` | Total matching items across all pages. |

`str(response)` and `repr(response)` produce `"<count> items"`.

## `StoreItem`

One inventory result in `StoreItemResponse.results`.

| Field               | Type        | Description                                   |
|---------------------|-------------|-----------------------------------------------|
| `item_name`         | `str`       | General item name, such as `"laptop"`.        |
| `long_icn`          | `str`       | The item's long ICN/barcode value.            |
| `details`           | `list[str]` | Item details, such as model and serial data.  |
| `price`             | `float`     | Item price.                                   |
| `distance`          | `float`     | Distance in miles from the search coordinate. |
| `category_desc`     | `str`       | Human-readable category description.          |
| `category_code`     | `str`       | Category code.                                |
| `is_available`      | `bool`      | Whether the item is available for purchase.   |
| `is_clearance_item` | `bool`      | Whether the item is marked as clearance.      |
| `store_number`      | `str`       | Number of the store holding the item.         |
| `store_short_name`  | `str`       | Short name of that store.                     |

The string representation combines the item name, title-cased details, and
price.

## `StoreDisplayInfo`

Returned by `searchStoresByGeoLocation()`.

| Field          | Type                       | Description                                              |
|----------------|----------------------------|----------------------------------------------------------|
| `phone`        | `str \| None`              | Store phone number, if supplied.                         |
| `hours`        | `TodaysStoreHours \| None` | Today's hours, if supplied.                              |
| `brand`        | `str`                      | Store brand, such as `"Cash America"` or `"First Cash"`. |
| `address`      | `StoreAddress`             | Store postal address.                                    |
| `distance`     | `float`                    | Distance in miles from the search coordinate.            |
| `latitude`     | `float`                    | Store latitude.                                          |
| `longitude`    | `float`                    | Store longitude.                                         |
| `store_number` | `str`                      | Store number/ID.                                         |
| `short_name`   | `str`                      | Short store name, often based on its number.             |

`str(store)` and `repr(store)` produce `"<brand> <store number>"`.

## `StoreDetails`

Returned by `fetchStore()`.

| Field          | Type                 | Description                               |
|----------------|----------------------|-------------------------------------------|
| `phone`        | `str`                | Store phone number.                       |
| `address`      | `StoreAddress`       | Store postal address.                     |
| `services`     | `list[str]`          | Services such as loans or gold purchases. |
| `weekly_hours` | `list[StoreHours]`   | Opening hours for each weekday.           |
| `licenses`     | `list[StoreLicense]` | Store licenses; often empty.              |
| `store_number` | `str`                | Store number/ID.                          |
| `short_name`   | `str`                | Short store name.                         |

`str(store)` and `repr(store)` return the uppercased short name.

## `StoreAddress`

Nested in `StoreDisplayInfo` and `StoreDetails`.

| Field      | Type          | Description                             |
|------------|---------------|-----------------------------------------|
| `address1` | `str`         | Primary street-address line.            |
| `address2` | `str \| None` | Secondary address line, usually `None`. |
| `state`    | `str`         | Two-letter state code.                  |
| `city`     | `str`         | City.                                   |
| `zip_code` | `str`         | ZIP code.                               |

Its string representation formats the fields as a one-line postal address.

## `TodaysStoreHours`

Nested in nearby-store results.

| Field          | Type   | Description                                   |
|----------------|--------|-----------------------------------------------|
| `open_time`    | `str`  | Opening time supplied by the API.             |
| `close_time`   | `str`  | Closing time supplied by the API.             |
| `is_open`      | `bool` | Whether the store is currently open.          |
| `display_text` | `str`  | Display-ready hours text supplied by the API. |
| `store_status` | `str`  | Status text such as `"Open"` or `"Closed"`.   |

`str(hours)` and `repr(hours)` produce
`"<open time> to <close time>"`.

## `StoreHours`

One entry in `StoreDetails.weekly_hours`.

| Field        | Type   | Description                                   |
|--------------|--------|-----------------------------------------------|
| `weekday`    | `str`  | Weekday represented by this entry.            |
| `open_time`  | `str`  | Opening time supplied by the API.             |
| `close_time` | `str`  | Closing time supplied by the API.             |
| `is_today`   | `bool` | Whether this entry describes the current day. |

`str(hours)` and `repr(hours)` produce
`"<weekday> <open time> to <close time>"`.

## `StoreLicense`

One entry in `StoreDetails.licenses`.

| Field             | Type  | Description                                   |
|-------------------|-------|-----------------------------------------------|
| `business_entity` | `str` | Licensed business entity returned by the API. |
| `license_number`  | `str` | License number.                               |
| `license_type`    | `str` | License type.                                 |

The upstream data commonly contains no license entries, and the field names
have not been confirmed against a populated response in this library.
