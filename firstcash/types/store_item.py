
class StoreItem:
    """An object for an item in a store."""

    item_name: str
    """The item's name. This will be what the item is, such as \"laptop,\" or \"shotgun.\""""

    long_icn: str
    """The item's ICN, or barcode value."""

    details: list[str]
    """The item's model and serial number."""

    price: float
    """The item's price."""

    distance: float
    """How far the store is from the specified latitude/longitude location."""

    category_desc: str
    """A description of the item's category."""

    category_code: str
    """The item's category code."""

    is_available: bool
    """A boolean value showing whether the item is available to purchase or not."""

    is_clearance_item: bool
    """Whether the item is on clearance or not."""

    store_number: str
    """The store number where the item is located."""

    store_short_name: str
    """The short name of the store where the item is located."""

    def __str__(self) -> str:
        return f"{self.item_name} {" ".title().join(self.details)} - ${self.price:.2f}"

    def __repr__(self) -> str:
        return str(self)
