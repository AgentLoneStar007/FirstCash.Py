class StoreHours:
    weekday: str
    """The day of the week that the contained hours pertain to. Example: ``Monday``."""

    open_time: str
    """The time that the store opens. Example: ``9:00 am``"""

    close_time: str
    """The time that the store closes. Example: ``7:00 pm``"""

    is_today: bool
    """A boolean value reflecting whether the specified weekday is today or not."""

    def __str__(self) -> str:
        return f"{self.weekday} {self.open_time} to {self.close_time}" if self.open_time.lower() != "closed" else f"Closed {self.weekday}"

    def __repr__(self) -> str:
        return str(self)
