from typing import Union
from constants.sql import CONSTANTS


# might be remove later
def quote(val: Union[int, float, str, list, type, list]):
    """
    Quotes control
    :param: Any val
    :return str(val) if value not (int or in CONSTANTS )
    """
    if isinstance(val, (int, float)) or val in CONSTANTS:
        return val

    elif isinstance(val, (list, tuple)) and len(val) == 1:
        return f'{val[0]}'

    else:
        return f'{val}'
