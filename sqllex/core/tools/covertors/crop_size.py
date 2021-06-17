from sqllex.debug import logger
from sqllex.types import Tuple, List, Union


def crop(columns: Union[Tuple, List], values: Union[Tuple, List]) -> Tuple:
    """
    Converts input lists (columns and values) to the same length for safe insert

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

    if values and columns:
        if len(values) != len(columns):
            logger.debug(
                f"\n"
                f"SIZE CROP! Expecting {len(columns)} arguments but {len(values)} were given!\n"
                f"Expecting: {columns}\n"
                f"Given: {values}"
            )
            _len_ = min(len(values), len(columns))
            return columns[:_len_], values[:_len_]

    return columns, values


__all__ = [
    'crop'
]
