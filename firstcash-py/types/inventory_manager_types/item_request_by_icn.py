class ItemRequestByICN:
    icns: list[str]
    unique_id: str
    search_term: str
    category_codes: list[str]
    search_price_high: float
    search_price_low: float
    longitude: float
    latitude: float
    search_distance: float  # why is this a float, you can't even select a floating-point number of miles on the website
