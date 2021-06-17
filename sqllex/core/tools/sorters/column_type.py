from sqllex.types import AnyStr, DataType, Union
from sqllex.constants import CONST_PRIORITY


def column_types(val: Union[DataType, AnyStr]) -> int:
    """
    Sorting function for DataType objects
    It's getting objects and returns index of priority (0,1,2,3)

    Parameters
    ----------
    val : Union[DataType, AnyStr]
        param of column type

    Returns
    -------
    int
        index of priority, if unknown returns 1

    """

    prior = CONST_PRIORITY.get(val)  # How about set dict.setdefault(1) ?

    if prior is None:
        return 1
    else:
        return prior
