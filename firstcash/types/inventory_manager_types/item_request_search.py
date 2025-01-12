class ItemRequestSearch:
    """A request for an item or items by store with options for minimum and maximum price
    ranges, locations specification, and category codes.
    """

    stores: list[str]
    """A list of stores to search through."""

    search_page: int
    """The index of the page of results."""

    results_per_page: int
    """The amount of items that should appear on each page."""

    only_clearance_items: bool
    """Whether only clearance items should be shown or not."""

    unique_id: str
    # TODO: Figure out what unique IDs are

    search_term: str
    """A string to search by. A type of item, such as \"laptop,\" would work best."""

    category_codes: list[str]
    """A list of category codes to search by."""

    search_price_high: float
    """The highest price of an item to include."""

    search_price_low: float
    """The lowest price of an item to include."""

    longitude: float
    """The search location longitude."""

    latitude: float
    """The search location latitude."""

    search_distance: float
    """The search radius, in miles, to search from the specified latitude/longitude."""
