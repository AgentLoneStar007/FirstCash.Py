from .store_item import StoreItem


class StoreItemResponse:
    """A response object for when an item is searched for by location."""

    def __init__(self) -> None:
        ## If this wasn't here, every instance of this object would share a results attribute.
        ## No idea why; I'm not a computer scientist.
        self.results = []

    results: list[StoreItem]
    """A list of items that match the provided query options."""

    number_pages_total: int
    """The total amount of pages of items that match the query."""

    number_items_total: int
    """The total amount of items that match the query."""

    def __str__(self) -> str:
        # TODO: Possibly revisit this or remove it
        return f"{self.number_items_total} items"

    def __repr__(self) -> str:
        return str(self)
