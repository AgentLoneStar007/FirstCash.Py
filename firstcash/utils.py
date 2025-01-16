from urllib.parse import urljoin, urlencode
from .exceptions import (SearchCoordinateValueError, SearchRadiusValueError, StoreIDValueError, CategoryCodeValueError,
                         PageIndexValueError, PageSizeValueError, PriceValueError)


# Function to build a URL to make a request to
def buildURL(base_api_url: str, api_key: str, endpoint: str = None, params: dict = None) -> str:
    """
    A function to build a URL that can be used to make an API request.

    :param base_api_url: The base URL of the API.
    :param api_key: The API key for the used API.
    :param endpoint: The endpoint to use. Optional.
     This will be something like "Categories," or "Items."
    :param params: The parameters to append to the URL, in a dictionary
     "key": "value" format.

    :returns: ``str`` - The URL to query with all provided parameters.

    :raises None:
    """

    # Create the base URL
    url: str = urljoin(base_api_url, endpoint) if endpoint else base_api_url

    if params:
        # Join the parameters to the base URL, if provided
        query_string: str = urlencode(params)
        if "?" not in url:
            url += "?" + query_string
        else:
            url += "&" + query_string

    # Append the API key to the end, using a & separator if any parameters were
    # provided, or a ? if none were provided
    url += f"{"&" if params else "?"}key={api_key}"

    return url


class ValueCheckers:
    @staticmethod
    def checkLatitude(latitude: float) -> None:
        """Checks a latitude coordinate to see if it's within bounds."""

        if not (-90 <= latitude <= 90):
            raise SearchCoordinateValueError(
                "A latitude value must be greater than or equal to -90, and less than or equal to 90.")

        return

    @staticmethod
    def checkLongitude(longitude: float) -> None:
        """Checks a longitude coordinate to see if it's within bounds."""

        if not (-180 <= longitude <= 180):
            raise SearchCoordinateValueError(
                "A longitude value must be greater than or equal to -180 and less than or equal to 180.")

        return

    @staticmethod
    def checkSearchRadius(search_radius: int | float) -> None:
        """Checks a search radius to see if it's within bounds."""

        if not (0 <= search_radius <= 5000):
            raise SearchRadiusValueError(
                "A search radius cannot be negative and must be less than or equal to 5,000 miles.")

        return

    @staticmethod
    def checkPriceFilters(max_price: float | int, min_price: float | int = None) -> None:
        """Checks price filters to see if they're within bounds."""

        if max_price < 0:
            raise PriceValueError("Price filters cannot be negative.")

        if min_price:
            if min_price < 0:
                raise PriceValueError("Price filters cannot be negative.")

            if max_price < min_price:
                raise PriceValueError("The maximum price filter cannot be less than the minimum price filter.")
        return

    @staticmethod
    def checkStoreID(store_id: int) -> None:
        """Checks a store ID to see if it's within bounds."""

        if not (0 <= store_id <= 32767):
            raise StoreIDValueError("A store ID cannot be negative and must be less than or equal to 32,767.")

        return

    @staticmethod
    def checkCategoryCode(category_code: int) -> None:
        """Checks a category code to see if it's within bounds."""

        if not (category_code >= 0):
            raise CategoryCodeValueError("Category codes cannot be negative.")

        return

    @staticmethod
    def checkPageIndex(index: int, starting_index: int = 0) -> None:
        """Checks a page index to see if it's within bounds."""

        if index < 0:
            raise PageIndexValueError("Page index cannot be negative.")

        ## While this is semi-unnecessary, it adds a bit of prettification to the error.
        if index < starting_index:
            raise PageIndexValueError("Page index below starting index.")

        return

    @staticmethod
    def checkPageSize(page_size: int) -> None:
        """Checks a page's size to see if it's within bounds."""

        if page_size <= 0:
            raise PageSizeValueError("The page size must be greater than or equal to one.")
