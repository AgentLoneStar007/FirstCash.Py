"""
FirstCash.Py
------------
A basic API wrapper for the FirstCash
mobile app API, which exposes the combined
functionality of the store and inventory
management APIs, allowing the user to fetch
store details as well as search for items across
the massive FirstCash inventory network.

:copyright: (c) 2026 AgentLoneStar007
:license: MIT
"""

__title__: str = "firstcash"
__author__: str = "AgentLoneStar007"
__license__: str = "MIT"
__copyright__: str = "Copyright © 2026-present AgentLoneStar007"
__version__: str = "1.0"

# Imports from library files, to make everything accessible under the main import of "firstcash"

from .api_client import APIClient
from .types.category import Category
from .types.store_address import StoreAddress
from .types.store_details import StoreDetails
from .types.store_display_info import StoreDisplayInfo
from .types.store_hours import StoreHours
from .types.store_item import StoreItem
from .types.store_item_response import StoreItemResponse
from .types.store_license import StoreLicense
from .types.todays_store_hours import TodaysStoreHours
from .exceptions import (
    FirstCashException, APIGeneralError, APIServerError, APIUnauthorizedError, APIResponseTimedOut, APIContentNotFound,
    APIRateLimited, SearchCoordinateValueError, SearchRadiusValueError, StoreIDValueError, CategoryCodeValueError,
    PageIndexValueError, PageSizeValueError, PriceValueError
)
