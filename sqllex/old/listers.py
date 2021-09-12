"""
Listers
"""
from sqllex.types import Any, List


def lister(data: Any, remove_one_len: bool = False) -> List:
    """
    Function converting input value from Tuple[Any] or List[Tuple]
    (with any deepness) to List[List]

    Parameters
    ----------
    data : Any
        Any value contains tuples
    remove_one_len : bool
        Convert or not [['x'], 1] to ['x', 1] (breaking return rule)

    Returns
    ----------
    callable
        Decorated method with update after it was run

    """

    if isinstance(data, tuple):
        data = list(data)

    if isinstance(data, list):
        if remove_one_len and (len(data) == 1):
            return lister(
                data[0],
                remove_one_len
            )

        for r in range(len(data)):
            if isinstance(data[r], (list, tuple)):
                data[r] = lister(
                    data[r],
                    remove_one_len
                )

    return data


def return2list(func: callable) -> callable:
    """
    Decorator converting returning data to List[List]

    Parameters
    ----------
    func : callable
        Function or method returns of with one need to convert from Tuple[Tuple[Any]] to List[List[Any]]

    Returns
    ----------
    callable
        Decorated method or func returning List[List]

    """

    def t2l_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        ret = lister(ret)

        if not isinstance(ret, list):
            ret = [ret]

        return ret

    return t2l_wrapper


def tuple2list(*args, **kwargs):
    data = lister(*args, **kwargs)

    if not isinstance(data, list):
        return [data]

    return data


__all__ = [
    'lister',
    'return2list',
    'tuple2list',
]
