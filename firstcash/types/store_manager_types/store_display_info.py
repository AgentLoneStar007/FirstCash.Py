from .todays_store_hours import TodaysStoreHours
from .store_address import StoreAddress


class StoreDisplayInfo:
    phone: str
    hours: TodaysStoreHours
    brand: str
    address: StoreAddress
    distance: float
    latitude: float
    longitude: float
    store_number: str
    short_name: str
