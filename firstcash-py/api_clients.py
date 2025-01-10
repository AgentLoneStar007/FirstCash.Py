# Import(s)
import requests
from urllib.parse import urljoin, urlencode
from .types.inventory_manager_types.category import Category


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
