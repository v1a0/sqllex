class TableInfoError(MemoryError):
    """
    Table doesn't exist or have no columns
    """
    def __str__(self):
        return "Table doesn't exist or have no columns"


__all__ = [
    "TableInfoError",
]
