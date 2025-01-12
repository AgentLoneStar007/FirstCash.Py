class StoreHours:
    weekday: str
    """The day of the week that the contained hours pertain to."""

    open_time: str
    """The time that the store opens."""

    close_time: str
    """The time that the store closes."""

    is_today: bool
    """A boolean value reflecting whether the specified weekday is today or not."""
