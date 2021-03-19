from typing import Any
import column_gens as cg


def args_fix(args: Any, kwargs: Any) -> tuple:
    """
    If args = (dict,) :return: (args, kwargs) = (None, dict)
    If args = (list,) :return: (args, kwargs) = (list, None)
    If args = (tuple,) :return: (args, kwargs) = (list, None)
    Otherwise :return: (args, kwargs)
    """
    if len(args) == 1:
        if isinstance(args[0], dict):
            return None, (args,)
        if isinstance(args[0], list):
            return (args[0],), None
        if isinstance(args[0], tuple):
            return (args[0],), None

    else:
        return args, kwargs


def args2list(args: Any) -> list:
    """
    Converting *args from tuple to list
    :param args: args
    :return: args as list
    """
    res = []
    for arg in args:
        res.append(
            cg.type_control(arg) if isinstance(arg, (str, int, float))
            else str(arg)
        )
    return res


def kwargs2lists(kwargs: dict) -> tuple:
    """
    Converting *kwargs from dict to ([keys], [values])
    :param kwargs: dict
    :return: ([keys], [values])
    """
    return list(kwargs.keys()), list(kwargs.values())
