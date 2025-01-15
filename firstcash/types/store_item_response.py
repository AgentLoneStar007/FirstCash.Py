from .store_item import StoreItem


class StoreItemResponse:
    """A response object for when an item is searched for by location."""

    results: list[StoreItem] = []
    """A list of items that match the provided query options."""

    number_pages_total: int
    """The total amount of pages of items that match the query."""

    number_items_total: int
    """The total amount of items that match the query."""
