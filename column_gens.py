from typing import Any, AnyStr, Mapping, Set, Union
from constants import *
from init_types import NumStr, ListDataType
from loguru import logger


def qtc(val: Union[int, float, str, list, type]):
    """
    Quotes ("str") control
    :param: Any val
    :return "str" if str not in CONSTANTS else str
    """
    if isinstance(val, (int, float)) or val in CONSTANTS:
        return f'{val}'

    elif isinstance(val, (list, tuple)) and len(val) == 1:
        return f'"{val[0]}"'
    
    else:
        return f'"{val}"'


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


def equalize_size(columns: list, values: list) -> tuple:
    if len(values) != len(columns):
        logger.warning(f"SIZE CROP! Expecting {len(columns)} arguments but {len(values)} were given!")
        if len(values) > len(columns):
            values = values[:len(columns)]
        if len(values) < len(columns):
            columns = columns[:len(values)]

    return columns, values
