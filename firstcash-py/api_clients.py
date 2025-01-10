# Import(s)
import requests
from urllib.parse import urljoin, urlencode


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
        A function

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
