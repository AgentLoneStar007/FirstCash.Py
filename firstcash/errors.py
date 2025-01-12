class FirstCashException(Exception):
    """Base exception for the entire library. All other exceptions
    are based on this one.
    """

    pass


class APIServerError(FirstCashException):
    """Error raised when there's an error on the APIs side."""

    def __init__(self, message: str) -> None:
        super().__init__(message)

        return


class ContentNotFound(FirstCashException):
    """Error raised when data could not be found."""

    def __init__(self, message: str) -> None:
        super().__init__(message)

        return
