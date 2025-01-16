class FirstCashException(Exception):
    """Base exception for the entire library. All other exceptions
    are based on this one.
    """

    pass


class APIServerError(FirstCashException):
    """Error raised when there's an error on the APIs side."""

    def __init__(self, message: str = None) -> None:
        if not message:
            message = "An error occurred in the FirstCash API."

        super().__init__(message)

        return


class ContentNotFound(FirstCashException):
    """Error raised when the requested data could not be found,
    or no matches were found for the query."""

    pass


class RateLimited(FirstCashException):
    """Error raised when the API rate limits connections."""

    pass


class SearchCoordinateValueError(FirstCashException):
    """Error raised when a latitude or longitude value is out of range."""

    pass


class SearchRadiusValueError(FirstCashException):
    """Error raised when a search radius value is out of range."""

    pass


class StoreIDValueError(FirstCashException):
    """Error raised when a store's ID is out of range."""

    pass


class CategoryCodeValueError(FirstCashException):
    """Error raised when a category code is out of range."""

    pass


class PageIndexValueError(FirstCashException):
    """Error raised when the page index is out of range."""

    pass


class PageSizeValueError(FirstCashException):
    """Error raised when the page size is out of range."""

    pass


class PriceValueError(FirstCashException):
    """Error raised when a minimum or maximum price value is out of range."""

    pass
