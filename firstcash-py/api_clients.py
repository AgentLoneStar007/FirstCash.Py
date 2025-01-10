# Import(s)
import requests
from urllib.parse import urljoin, urlencode
from .types.inventory_manager_types.category import Category
from types.inventory_manager_types.store_item import StoreItem
from types.inventory_manager_types.store_item_response import StoreItemResponse


# The API client for FirstCash's inventory management system
class InventoryAPIClient:
    def __init__(self, api_key: str) -> None:
        # Define the base URL for the inventory management API
        self.api_base_url: str = "https://search.cashamerica.com/api/"

        # Define class-wide variable(s)
        self.api_key: str = api_key

        return

    def _buildURL(self, endpoint: str, params: dict = None) -> str:
        """
        A function to build a URL that can be used to make an API request.

        :param endpoint: The endpoint to use. This will be something like
         "Categories," or "Items."
        :param params: The parameters to append to the URL, in a dictionary
         "key": "value" format.

        :returns: ``str`` - The URL to query with all provided parameters.

        :raises None:
        """

        # Create the base URL
        url: str = urljoin(self.api_base_url, endpoint)

        if params:
            # Join the parameters to the base URL, if provided
            query_string: str = urlencode(params)
            if "?" not in url:
                url += "?" + query_string
            else:
                url += "&" + query_string

        # Append the API key to the end, using a & separator if any parameters were
        # provided, or a ? if none were provided
        url += f"{"&" if params else "?"}key={self.api_key}"

        return url

    async def fetchCategories(self) -> list[Category]:
        """
        Fetches a list of categories.

        :returns: ``list[Category]`` - A list of Categories.

        :raises None: (temporarily)
        """

        try:
            # Make the API request
            response: requests.Response = requests.get(self._buildURL(endpoint="Categories"))
            response.raise_for_status()
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

        :raises None: (temporarily)
        """
        # TODO: Determine what this API call actually does, and what it's
        #  purpose is.

        try:
            # Make the API request
            response: requests.Response = requests.get(
                self._buildURL(endpoint="Categories/top"))
            response.raise_for_status()
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

    async def fetchItems(self, category_code: int,
                         search_latitude: float,
                         search_longitude: float,
                         search_radius: float,
                         page_index: int = 0,
                         page_size: int = 10,
                         unique_id: str = None,
                         search_term: str = None
                         ) -> StoreItemResponse:
        """
        A function to fetch a list of items.

        :param category_code: The category code to search by.
         Default is zero, which is all categories.
        :param search_latitude: The latitude to search from.
        :param search_longitude: The longitude to search from
        :param search_radius: The radius to search from.
        :param page_index: The index of the page to start on.
         Optional. Default is zero(first page).
        :param page_size: The amount of items on each page.
         Optional. Default is ten.
        :param unique_id: The unique ID to use. Optional.
        :param search_term: The search term to use. Optional.

        :returns: ``StoreItemResponse``

        :raises None: (temporarily)
        """

        try:
            # Make the API request
            response: requests.Response = requests.get(
                self._buildURL(endpoint="Items"), params={
                    "c": category_code,
                    "p": page_index,
                    "s": page_size,
                    "lat": search_latitude,
                    "lng": search_longitude,
                    "r": search_radius,
                    "u": unique_id if unique_id else "null",
                    "t": search_term if search_term else ""
                })
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            # TODO: Add API errors
            raise

        # Grab the data out of the response
        data: dict = response.json()

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


# The API client for FirstCash's store interface
class StoreAPIClient:
    def __init__(self, api_key: str) -> None:
        # Define the base URL for the store management API
        self.api_base_url: str = "http://find.cashamerica.us/api/"

        # Define class-wide variable(s)
        self.api_key: str = api_key

        return

    def _buildURL(self, endpoint: str, params: dict = None) -> str:
        """
        A function to build a URL that can be used to make an API request.

        :param endpoint: The endpoint to use. This will be something like
         "Categories," or "Items."
        :param params: The parameters to append to the URL, in a dictionary
         "key": "value" format.

        :returns: ``str`` - The URL to query with all provided parameters.

        :raises None:
        """

        # Create the base URL
        url: str = urljoin(self.api_base_url, endpoint)

        if params:
            # Join the parameters to the base URL, if provided
            query_string: str = urlencode(params)
            if "?" not in url:
                url += "?" + query_string
            else:
                url += "&" + query_string

        # Append the API key to the end, using a & separator if any parameters were
        # provided, or a ? if none were provided
        url += f"{"&" if params else "?"}key={self.api_key}"

        return url
