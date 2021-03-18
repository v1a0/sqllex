from typing import Any, AnyStr, Mapping
from constants import *
from init_types import NumStr, ListDataType


def qtc(param: Any):
    """
    Quotes control
    int = int
    str = "str" if str not in CONSTANTS else str
    """
    if param not in CONSTANTS and type(param) == str:
        return f'"{param}"'
    else:
        return f'{param}'


def simple(col: AnyStr, params: NumStr) -> AnyStr:
    return f"{col} {qtc(params)}" + ',\n'


def compound(col: AnyStr, params: ListDataType) -> AnyStr:
    res = f"{col}"
    for param in params:
        res += f' {qtc(param)}'

    return f"{res},\n"


def mapped(col: AnyStr, params: Mapping) -> AnyStr:
    if col == FOREIGN_KEY:
        return foreign_key(params)
    else:
        raise TypeError


def foreign_key(params: Mapping) -> AnyStr:
    """
    DOES NOT WORK ! (ikd why)
    :param params:
    :return:
    """
    res = ''
    for (key, refs) in params.items():
        res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
        # for ref in refs[2:]:
        #     res += f" {ref}"

    return res[:-1]

