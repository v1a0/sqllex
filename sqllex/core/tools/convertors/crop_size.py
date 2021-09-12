from sqllex.types import Tuple, List, Union


def crop(columns: Union[Tuple, List], values: Union[Tuple, List]) -> Tuple:
    """
    Converts input lists (columns and values) to the same length for safe insert

    +-------------+
    | WEIRD STUFF |
    +-------------+- v1a0

    Parameters
    ----------
    columns : Union[Tuple, List]
        List of columns in some table
    values : Union[Tuple, List]
        Values for insert to some table

    Returns
    ----------
        Equalized by length lists

    """
    val_len, col_len = len(values), len(columns)

    if val_len != col_len:
        _len_ = min(val_len, col_len)
        return columns[:_len_], values[:_len_]

    return columns, values


__all__ = [
    'crop'
]
