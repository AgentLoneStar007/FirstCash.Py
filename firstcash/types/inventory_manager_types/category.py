class Category:
    """Represents a category, with a code and a name."""

    category_code: str
    """The category's code."""

    category_name: str
    """The category's name."""

    parent_id: str | None
    """The category's parent ID. Might be NoneType."""

    has_children: bool
    """A boolean value showing whether the category has children."""
