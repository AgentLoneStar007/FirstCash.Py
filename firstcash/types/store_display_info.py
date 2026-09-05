from .todays_store_hours import TodaysStoreHours
from .store_address import StoreAddress


class StoreDisplayInfo:
    phone: str | None
    """The store's phone number. In rare cases, this will be NoneType."""

    hours: TodaysStoreHours | None
    """The time that the store is open today. In rare cases, this will be NoneType."""

    brand: str
    """The store's brand. This will be something like \"Cash America,\" or \"First Cash.\""""

    address: StoreAddress
    """An address object for the store."""

    distance: float
    """The distance, in miles, that the store is from the provided latitude/longitude."""

    latitude: float
    """The store's latitude."""

    longitude: float
    """The store's longitude."""

    store_number: str
    """The store's number, or ID."""

    short_name: str
    """The store's name. This will usually be something like \"fcp(store number).\""""

    def __str__(self) -> str:
        # When this object is printed as a string, it will be in the format of
        # (store brand) (store number), such as "National Pawn 4412"
        return f"{self.brand} {self.store_number}"

    def __repr__(self) -> str:
        return str(self)
