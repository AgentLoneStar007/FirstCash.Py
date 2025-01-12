from .store_address import StoreAddress
from .store_hours import StoreHours
from .store_license import StoreLicense


class StoreDetails:
    phone: str
    address: StoreAddress
    services: list[str]
    weekly_hours: list[StoreHours]
    licenses: list[StoreLicense]
    store_number: str
    short_name: str
