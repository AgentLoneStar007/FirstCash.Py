from .store_address import StoreAddress
from .store_hours import StoreHours
from .store_license import StoreLicense


class StoreDetails:
    phone: str
    """The store's phone number."""

    address: StoreAddress
    """An address object for the store."""

    services: list[str]
    """A list of services that the store provided, such as loans, gold purchases, etc."""

    weekly_hours: list[StoreHours]
    """A list of hours that the store is open on each weekday."""

    licenses: list[StoreLicense]
    """A list of licenses that the store possesses. A lot of times this will be empty."""

    store_number: str
    """The store's number, or ID."""

    short_name: str
    """The store's name. This will usually be something like \"fcp(store number).\""""

    def __str__(self) -> str:
        return self.short_name.upper()

    def __repr__(self) -> str:
        return str(self)
