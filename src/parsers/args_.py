from typing import Any


def argfix(args: Any, kwargs: Any) -> tuple:
    """
    If args = (dict,) :return: (args, kwargs) = (None, dict)
    If args = (list,) :return: (args, kwargs) = (list, None)
    If args = (tuple,) :return: (args, kwargs) = (list, None)
    Otherwise :return: (args, kwargs)
    """

    if len(args) == 1:
        if isinstance(args[0], dict):
            return None, args[0]
        if isinstance(args[0], list):
            return tuple(args[0]), None
        if isinstance(args[0], tuple):
            return args[0], None
        else:
            return args, None

    else:
        return args, kwargs

