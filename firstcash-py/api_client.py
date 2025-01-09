import requests
#from .exceptions import


class APIClient:
    def __init__(self, api_key: str) -> None:
        # Define the base URL for both the store and inventory management APIs
        self.inventory_api_base_url: str = "https://search.cashamerica.com/api/"
        self.store_api_base_url: str = "http://find.cashamerica.us/api/"

        # Define class-wide variable(s)
        self.api_key: str = api_key

        return

    def _buildURL(self, endpoint, params=None) -> str:
        """

        :param endpoint:
        :param params:

        :returns: ``str`` - The URL to query with all provided parameters.

        :raises None:
        """
