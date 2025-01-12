from .store_item import StoreItem


class StoreItemResponse:
    results: list[StoreItem] = []
    number_pages_total: int
    number_items_total: int
