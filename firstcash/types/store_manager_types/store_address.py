class StoreAddress:
    address1: str
    """The store's street address."""

    address2: str | None
    """A secondary line for the store's address. Usually this is NoneType."""

    state: str
    """The two-letter state code where the store resides."""

    city: str
    """The city where the store is located."""

    zip_code: str
    """The zip code where the store is located."""
