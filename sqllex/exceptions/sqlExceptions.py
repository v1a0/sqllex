class TableInfoError(MemoryError):
    """
    ABTable doesn't exist or have no columns
    """
    def __str__(self):
        return "ABTable doesn't exist or have no columns"


__all__ = [
    "TableInfoError",
]
