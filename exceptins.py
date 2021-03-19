class TableInfoError(Exception):
    """
    Table doesn't exist or have no columns
    """
    def __str__(self):
        return "Table doesn't exist or have no columns"


class ExecuteError(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        s = '\n'
        for (arg, kwarg) in self.kwargs.items():
            s += f"{arg}: {kwarg}\n"
        return s
