# Import(s)
import requests
from urllib3.exceptions import MaxRetryError
from json import JSONDecodeError
from .utils import buildURL
from .utils import ValueCheckers as value_checkers
from .types.category import Category
from .types.store_item import StoreItem
from .types.store_item_response import StoreItemResponse
from .types.store_display_info import StoreDisplayInfo
from .types.todays_store_hours import TodaysStoreHours
from .types.store_address import StoreAddress
from .types.store_details import StoreDetails
from .types.store_hours import StoreHours
from .types.store_license import StoreLicense
from .exceptions import *


# The main class for the entire library
class APIClient:
    def __init__(self, api_key: str) -> None:
        # Define the base URL for the inventory management API
        self._api_base_url: str = "https://mobileapps.cashamerica.com/api/v2/"

        # Define class-wide variable(s)
        self._api_key: str = api_key

        return

    # TODO: Find a way to censor the API key in exceptions

    async def fetchCategories(self) -> list[Category]:
        """
        Fetches a list of categories.

        :returns: ``list[Category]`` - A list of Categories.

        :raises RateLimited: If your request is rate-limited by the API.
        :raises None: (temporarily)
        """

        try:
            # Make the API request
            response: requests.Response = requests.get(
                buildURL(base_api_url=self._api_base_url, api_key=self._api_key, endpoint="Categories")
            )
            response.raise_for_status()

        # Max retry error is raised when the API rate limits you
        except MaxRetryError:
            raise RateLimited

        except requests.exceptions.RequestException as error:
            # TODO: Add API errors
            raise

        # Grab the data out of the response
        data: dict = response.json()

        # Create a list of data that will be returned
        return_list: list[Category] = []

        # Go through each category, create a Category object, set the object's
        # data, and add it to the return list
        for item in data:
            category: Category = Category()
            category.category_code = item["categoryCode"]
            category.category_name = item["categoryName"]
            category.parent_id = item["parentID"]
            category.has_children = item["hasChildren"]

            # Append the category to the return list
            return_list.append(category)

        return return_list

    ## Not exactly sure what the function is of this API call, but hey, it's there
    async def fetchTopCategories(self) -> list[Category]:
        """
        Fetch top-level categories.

        :returns: ``list[Category]`` - A list of categories.

        :raises RateLimited: If your request is rate-limited by the API.
        :raises None: (temporarily)
        """

        try:
            # Make the API request
            response: requests.Response = requests.get(
                buildURL(base_api_url=self._api_base_url, api_key=self._api_key, endpoint="Categories/top"))
            response.raise_for_status()

        except MaxRetryError:
            raise RateLimited

        except requests.exceptions.RequestException as error:
            # TODO: Add API errors
            raise

        # Grab the data out of the response
        data: dict = response.json()

        # Create a list that will be returned
        return_list: list[Category] = []

        # Go through each returned category
        for category_json in data:
            # Create a Category object for it
            category: Category = Category()

            # Assign the object's attributes
            category.category_code = category_json["categoryCode"]
            category.category_name = category_json["categoryName"]
            category.parent_id = category_json["parentID"]
            category.has_children = category_json["hasChildren"]

            # And add it to the list to be returned
            return_list.append(category)

        return return_list

    async def searchItemsByGeoLocation(self, category_code: int,
                                       search_latitude: float,
                                       search_longitude: float,
                                       search_radius: float,
                                       page_index: int = 0,
                                       page_size: int = 10,
                                       search_term: str = None
                                       ) -> StoreItemResponse:
        """
        A function to search for an item by location.

        :param category_code: The category code to search by.
         Default is zero, which is all categories. Cannot
         be negative.
        :param search_latitude: The latitude to search from.
         Cannot be less than -90 or greater than 90.
        :param search_longitude: The longitude to search from
         Cannot be less than -180 or greater than 180.
        :param search_radius: The radius from the specified
         location to search from. Cannot be negative or
         greater than 5,000.
        :param page_index: The index of the page to start on.
         Optional. Default is zero(first page). Cannot be
         negative.
        :param page_size: The amount of items on each page.
         Optional. Default is ten. Cannot be negative or zero.
        :param search_term: The search term to use. This will be
         something like "laptop," or "purse." Optional.

        :returns: ``StoreItemResponse`` - A store item response
         object, which includes a list of results and other info.

        :raises CategoryCodeValueError: If a category code is non-numerical
         or negative.
        :raises SearchCoordinateValueError: If latitude is less than -90
         or greater than 90, or longitude is less than -180 or greater
         than 180.
        :raises SearchRadiusValueError: If the search radius is negative
         or greater than 5,000.
        :raises PageIndexValueError: If the page index is negative.
        :raises PageSizeValueError: If the page size is zero or less.
        :raises RateLimited: If your request is rate-limited by the API.
        :raises APIServerError: If the API returns a 500 HTTP response code,
         indicating an internal server error.
        :raises ContentNotFound: If the API couldn't find any items matching the query.
        """

        # Check the provided coordinates
        value_checkers.checkLatitude(search_latitude)
        value_checkers.checkLongitude(search_longitude)

        # Check the page index and size
        value_checkers.checkPageIndex(page_index)
        value_checkers.checkPageSize(page_size)

        try:
            # Make the API request
            response: requests.Response = requests.get(
                buildURL(base_api_url=self._api_base_url, api_key=self._api_key, endpoint="Items"), params={
                    "c": category_code,
                    "p": page_index,
                    "s": page_size,
                    "lat": search_latitude,
                    "lng": search_longitude,
                    "r": search_radius,
                    "t": search_term if search_term else ""
                })
            response.raise_for_status()

        except MaxRetryError:
            raise RateLimited

        # Handle a non-200 response code
        except requests.exceptions.RequestException as error:
            raise APIServerError(f"Failed to search for items by location with the following error: {error}")

        try:
            # Grab the data out of the response
            data: dict = response.json()

        # Handle if there was an empty response(no matches)
        except JSONDecodeError:
            raise ContentNotFound("No items matched the query.")

        # Create the store item response object
        store_item_response: StoreItemResponse = StoreItemResponse()

        # Set the total number of pages and items
        store_item_response.number_pages_total = data["numberPagesTotal"]
        store_item_response.number_items_total = data["numberItemsTotal"]

        # Handle if there were no matching items
        if len(data["results"]) >= 1:
            # Go through each item in the response
            for item in data["results"]:
                # Create the item's object
                store_item: StoreItem = StoreItem()

                # Set the object's attributes
                store_item.item_name = item["itemName"]
                store_item.long_icn = item["longICN"]
                store_item.details = item["details"]
                store_item.price = item["price"]
                store_item.distance = item["distance"]
                store_item.category_desc = item["categoryDesc"]
                store_item.category_code = item["categoryCode"]
                store_item.is_available = item["isAvailable"]
                store_item.is_clearance_item = item["isClearanceItem"]
                store_item.store_number = item["storeNumber"]
                store_item.store_short_name = item["shortName"]

                # Add the item to the results list
                store_item_response.results.append(store_item)

        else:
            store_item_response.results = []

        return store_item_response

    async def searchItems(self, search_term: str,
                          search_latitude: float,
                          search_longitude: float,
                          search_radius: float,
                          search_price_high: float,
                          search_price_low: float = None,
                          stores: list[str] = None,
                          category_codes: list[str] = None,
                          page_index: int = 0,
                          page_size: int = 10,
                          only_clearance_items: bool = False
                          ) -> StoreItemResponse:
        """
        A function to search for items by location with the option to filter
        your search to multiple categories, specific stores, and set minimum
        and maximum price values for the items.

        :param search_term: The search term to use. This will be
         something like "laptop," or "purse." While this is
         unnecessary because you can specify your category
         code, it's still required for this request type.
         Cannot be blank.
        :param search_latitude: The latitude to search from.
         Cannot be less than -90 or greater than 90.
        :param search_longitude: The longitude to search from.
         Cannot be less than -180 or greater than 180.
        :param search_radius: The radius from the specified
         location to search from. Cannot be negative or
         greater than 5,000.
        :param search_price_high: The maximum price value for
         your query.
        :param search_price_low: The minimum price value for
         your query. Optional. Cannot be negative.
        :param stores: A list of store IDs in string format
         that you wish to limit your search by. Optional.
         Must be numerical, and cannot be negative or greater
         than 32,767.
        :param category_codes: A list of category codes in
         string format that you wish to limit your search
         by. Optional. Must be numerical, and cannot be negative.
        :param page_index: The index of the page to start on.
         Optional. Default is zero(first page). Cannot be negative.
        :param page_size: The amount of items on each page.
         Optional. Default is ten. Cannot be negative.
        :param only_clearance_items: A boolean value reflecting
         whether you only want clearance items included in your
         search. Optional. Default is false.

        :returns: ``StoreItemResponse`` - A store item response
         object, which includes a list of results and other info.

        :raises ValueError: If the search term was left blank.
        :raises SearchCoordinateValueError: If latitude is less than -90
         or greater than 90, or longitude is less than -180 or greater
         than 180.
        :raises SearchRadiusValueError: If the search radius is negative
         or greater than 5,000.
        :raises PriceValueError: If either price argument is negative, or if
         the minimum price is higher than the maximum price.
        :raises StoreIDValueError: If the store ID is non-numerical, negative,
         or greater than 32,767.
        :raises CategoryCodeValueError: If a category code is non-numerical
         or negative.
        :raises PageIndexValueError: If the page index is negative.
        :raises PageSizeValueError: If the page size is zero or less.
        :raises RateLimited: If your request is rate-limited by the API.
        :raises APIServerError: If the API returns a 500 HTTP response code,
         indicating an internal server error.
        :raises ContentNotFound: If the API couldn't find any items matching the query.
        """

        # Check if the search term is blank
        if not bool(search_term):
            raise ValueError("Search term cannot be blank in the searchItems method.")

        # Check the provided coordinates
        value_checkers.checkLatitude(search_latitude)  # if you can read this, go take geography again ;)
        value_checkers.checkLongitude(search_longitude)

        # Check the page index and size
        value_checkers.checkPageIndex(page_index)
        value_checkers.checkPageSize(page_size)

        # Check the price filters
        value_checkers.checkPriceFilters(search_price_high, search_price_low)

        # Assign the default empty list for stores if no list was specified
        if not stores:
            stores = []
        else:
            # Check each store ID to make sure it's acceptable
            for store_id in stores:
                # Handle if the store ID isn't an integer
                if not store_id.isnumeric():
                    raise StoreIDValueError("Store IDs must be numerical.")

                # Check if the store ID is within bounds
                value_checkers.checkStoreID(int(store_id))

        # Assign the default empty list for category codes if no list was specified
        if not category_codes:
            category_codes = []
        else:
            # Check each category code to make sure it's acceptable
            for category_code in category_codes:
                # Handle if the category code isn't an integer
                if not category_code.isnumeric():
                    raise CategoryCodeValueError("Category codes must be numerical.")

                value_checkers.checkCategoryCode(int(category_code))

        # Check to see if the search radius is within bounds
        value_checkers.checkSearchRadius(search_radius)

        try:
            response: requests.Response = requests.put(
                url=buildURL(
                    base_api_url="https://mobileapps.cashamerica.com/api/v2/",
                    api_key=self._api_key,
                    endpoint="Items"
                ), json={
                    "UniqueId": "firstcash-py",  # string, required, can be anything but can't be blank
                    "SearchTerm": search_term,  # string, required
                    "Stores": stores,  # list of string, can be empty
                    "CategoryCodes": category_codes,  # list of string, can be empty
                    "SearchPriceHigh": search_price_high,  # float, non-negative, required
                    "SearchPriceLow": search_price_low if search_price_low else 0,  # float, non-negative
                    "Longitude": search_longitude,  # float, required
                    "Latitude": search_latitude,  # float, required
                    "SearchDistance": search_radius,  # int, required
                    "SearchPage": page_index,  # int, required, zero-index
                    "ResultsPerPage": page_size,  # int, required
                    "OnlyClearanceItems": only_clearance_items  # bool
                })

            response.raise_for_status()

        except MaxRetryError:
            raise RateLimited

        # Handle a non-200 response code
        except requests.exceptions.RequestException as error:
            raise APIServerError(f"Failed to search for items by location with the following error: {error}")

        try:
            # Grab the data out of the response
            data: dict = response.json()

        # Handle if there was an empty response(no matches)
        except JSONDecodeError:
            # TODO: Find a better way to clarify whether there were no matches or the page index
            #  was out of range of the total pages.
            raise ContentNotFound("No items matched the query.")

        # Create the store item response object
        store_item_response: StoreItemResponse = StoreItemResponse()

        # Set the total number of pages and items
        store_item_response.number_pages_total = data["numberPagesTotal"]
        store_item_response.number_items_total = data["numberItemsTotal"]

        # Handle if there were no matching items
        if len(data["results"]) >= 1:
            # Go through each item in the response
            for item in data["results"]:
                # Create the item's object
                store_item: StoreItem = StoreItem()

                # Set the object's attributes
                store_item.item_name = item["itemName"]
                store_item.long_icn = item["longICN"]
                store_item.details = item["details"]
                store_item.price = item["price"]
                store_item.distance = item["distance"]
                store_item.category_desc = item["categoryDesc"]
                store_item.category_code = item["categoryCode"]
                store_item.is_available = item["isAvailable"]
                store_item.is_clearance_item = item["isClearanceItem"]
                store_item.store_number = item["storeNumber"]
                store_item.store_short_name = item["shortName"]

                # Add the item to the results list
                store_item_response.results.append(store_item)

        else:
            store_item_response.results = []

        return store_item_response

    async def searchStoresByGeoLocation(self,
                                        search_latitude: float,
                                        search_longitude: float,
                                        page_index: int = 1,
                                        page_size: int = 10
                                        ) -> list[StoreDisplayInfo]:
        """
        A function to search for stores near the specified latitude and longitude.

        :param search_latitude: The latitude to search from.
         Cannot be less than -90 or greater than 90.
        :param search_longitude: The longitude to search from
         Cannot be less than -180 or greater than 180.
        :param page_index: The index of which page to show. Optional.
         Default is one(the first page).
        :param page_size: How many items to show on each page. Optional.
         Default is ten.

        :returns: ``list[StoreDisplayInfo]`` - A list of store information.

        :raises SearchCoordinateValueError: If latitude is less than -90
         or greater than 90, or longitude is less than -180 or greater
         than 180.
        :raises PageIndexValueError: If the page index is negative.
        :raises PageSizeValueError: If the page size is zero or less.
        :raises RateLimited: If your request is rate-limited by the API.
        :raises APIServerError: If the API returns a 500 HTTP response code,
         indicating an internal server error.
        :raises ContentNotFound: If the API couldn't find any stores matching the query.
        """

        # Check the provided coordinates
        value_checkers.checkLatitude(search_latitude)
        value_checkers.checkLongitude(search_longitude)

        # Check the page index and size
        value_checkers.checkPageIndex(page_index, starting_index=1)
        value_checkers.checkPageSize(page_size)

        try:
            # Make the API request
            response: requests.Response = requests.get(
                buildURL(base_api_url=self._api_base_url, api_key=self._api_key, endpoint="Stores"), params={
                    "p": page_index,
                    "s": page_size,
                    "lat": search_latitude,
                    "lng": search_longitude
                })
            response.raise_for_status()

        except MaxRetryError:
            raise RateLimited

        # Handle a non-200 response code
        except requests.exceptions.RequestException as error:
            raise APIServerError(f"Failed to find a store by location with the following error: {error}")

        try:
            # Grab the data out of the response
            data: dict = response.json()

        # Handle if there was an empty response(no matches)
        except JSONDecodeError:
            # TODO: Find a better way to clarify whether there were no matches or the page index
            #  was out of range of the total pages.
            raise ContentNotFound("No stores matched the query.")

        # Handle if there were no matching items
        if len(data) >= 1:
            # Create the list to be returned
            return_list: list[StoreDisplayInfo] = []

            # Go through each item in the response
            for item in data:
                # Create the item's object
                store_info: StoreDisplayInfo = StoreDisplayInfo()

                # Create a store hours object for this store
                today_store_hours: TodaysStoreHours = TodaysStoreHours()

                # Set it's attributes
                today_store_hours.open_time = item["hours"]["openTime"]
                today_store_hours.close_time = item["hours"]["closeTime"]
                today_store_hours.is_open = item["hours"]["isOpen"]
                today_store_hours.display_text = item["hours"]["displayText"]
                today_store_hours.store_status = item["hours"]["storeStatus"]

                # Create a store address object for this store
                store_address: StoreAddress = StoreAddress()

                # Set it's attributes
                store_address.address1 = item["address"]["address1"]
                store_address.address2 = item["address"]["address2"]
                store_address.state = item["address"]["state"]
                store_address.city = item["address"]["city"]
                store_address.zip_code = item["address"]["zipCode"]

                # Set the store's attributes
                store_info.phone = item["phone"]
                store_info.hours = today_store_hours
                store_info.brand = item["brand"]
                store_info.address = store_address
                store_info.distance = item["distance"]
                store_info.latitude = item["latitude"]
                store_info.longitude = item["longitude"]
                store_info.store_number = item["storeNumber"]
                store_info.short_name = item["shortName"]

                # Add the store to the list to be returned
                return_list.append(store_info)

        else:
            # Return an empty list if no stores matched the query
            return []

        return return_list

    async def fetchStore(self, store_id: int) -> StoreDetails:
        """
        A function to fetch a singular store by its ID.

        :param store_id: The ID of the store. This will be the store's number.

        :returns: ``StoreDetails`` - A store details object, which will contain
         the info such as the address, phone number, etc.

        :raises StoreIDValueError: If the store ID is negative or greater than 32,767.
        :raises APIServerError: If the API returns a 500 HTTP response code,
         indicating an internal server error.
        :raises RateLimited: If your request is rate-limited by the API.
        :raises ContentNotFound: If the API couldn't find a store with a matching ID.
        """

        # Check the provided store ID
        value_checkers.checkStoreID(store_id)

        try:
            # Make the API request
            response: requests.Response = requests.get(
                buildURL(base_api_url=self._api_base_url, api_key=self._api_key, endpoint="Stores"), params={
                    "id": store_id
                })
            response.raise_for_status()

        except MaxRetryError:
            raise RateLimited

        # Handle a non-200 response code
        except requests.exceptions.RequestException as error:
            raise APIServerError(f"Failed to fetch a store by ID from the API with the following error: {error}")

        try:
            # Grab the data out of the response
            data: dict = response.json()

        # Handle if there was an empty response(no match)
        except JSONDecodeError:
            raise ContentNotFound("No store matched the provided ID.")

        # Create a store address object
        store_address: StoreAddress = StoreAddress()

        # Assign its attributes
        store_address.address1 = data["address"]["address1"]
        ## The second store address field can be blank, but it should be null
        store_address.address2 = data["address"]["address2"] if data["address"]["address2"] else None
        store_address.state = data["address"]["state"]
        store_address.city = data["address"]["city"]
        store_address.zip_code = data["address"]["zipCode"]

        # Create a list of store hours for this store
        store_hours_list: list[StoreHours] = []

        # Create a store hours object for each week day
        for weekday in data["weeklyHours"]:
            store_hours: StoreHours = StoreHours()

            store_hours.weekday = weekday["weekDay"]
            store_hours.open_time = weekday["openTime"]
            store_hours.close_time = weekday["closeTime"]
            store_hours.is_today = weekday["isToday"]

            # Add this store hours object to the list
            store_hours_list.append(store_hours)

        # Create a list for the store's licenses
        store_licenses: list[StoreLicense] = []

        # Create a license object for each store license
        for store_license in data["licenses"]:
            store_license_object: StoreLicense = StoreLicense()

            ## These are purely estimation as to the names of these values. I haven't
            ## seen a licensed listed for a store yet.
            store_license_object.business_entity = store_license["businessEntity"]
            store_license_object.license_number = store_license["licenseNumber"]
            store_license_object.license_type = store_license["licenseType"]

            # Append this license to the list of store licenses
            store_licenses.append(store_license)

        # Create a store details object
        store_details: StoreDetails = StoreDetails()

        # And assign its attributes
        store_details.phone = data["phone"]
        store_details.address = store_address
        store_details.services = data["services"]
        store_details.weekly_hours = store_hours_list
        store_details.licenses = store_licenses
        store_details.store_number = data["storeNumber"]
        store_details.short_name = data["shortName"]

        return store_details
