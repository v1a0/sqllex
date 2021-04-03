class TableInfoError(Exception):
    """
    Table doesn't exist or have no columns
    """
    def __str__(self):
        return "Table doesn't exist or have no columns"


class UniversalException(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        s = '\n'
        for (arg, kwarg) in self.kwargs.items():
            s += f"{arg}: {kwarg}\n"
        return s


class ExecuteError(UniversalException):
    """
    Execution failed by some reason, more
    """


class ArgumentError(UniversalException):
    """
    Argument have an incorrect type or value
    """
    pass


__all__ = [
    "TableInfoError",
    "UniversalException",
    "ExecuteError",
    "ArgumentError"
]
