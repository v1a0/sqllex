from py2sql.type_control import quote
from typing import AnyStr, Any
from constants.sql import *


def table(col: AnyStr, params: Any):
    if isinstance(params, list):
        return f"{col} {' '.join(quote(param) for param in params)},\n"

    elif isinstance(params, (int, str, float)):
        return f"{col} {quote(params)}" + ',\n'

    if isinstance(params, dict) and col == FOREIGN_KEY:
        res = ''
        for (key, refs) in params.items():
            res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
        return res[:-1]

    else:
        raise TypeError

