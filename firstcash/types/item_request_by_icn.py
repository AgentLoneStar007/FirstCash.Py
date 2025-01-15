class ItemRequestByICN:
    """A request for an item by ICN or multiple ICNs, with options for minimum and maximum price ranges,
    locations specification, and category code.
    """

    icns: list[str]
    """A list of items with a matching ICN."""

    unique_id: str
    # TODO: Figure out what the unique ID is

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
