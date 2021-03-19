from typing import Any, AnyStr, Mapping, Set, Union
from constants import *
from init_types import NumStr, ListDataType
from loguru import logger


def type_control(val: Union[int, float, str, list, type, list]):
    """
    Type control
    :param: Any val
    :return str(val) if value not (int or in CONSTANTS )
    """
    if isinstance(val, (int, float)) or val in CONSTANTS:
        return val

    elif isinstance(val, (list, tuple)) and len(val) == 1:
        return f'{val[0]}'

    else:
        return f'{val}'


def qtc_foreach(_list: Union[list, tuple]):
    for i in range(len(_list)):
        _list[i] = type_control(_list[i])
    return _list


def simple(col: AnyStr, params: NumStr) -> AnyStr:
    return f"{col} {type_control(params)}" + ',\n'


def compound(col: AnyStr, params: ListDataType) -> AnyStr:
    res = f"{col}"
    for param in params:
        res += f' {type_control(param)}'
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


def crop(columns: tuple, args: tuple) -> tuple:
    if len(args) != len(columns):
        logger.warning(f"SIZE CROP! Expecting {len(columns)} arguments but {len(args)} were given!")
        _len_ = min(len(args), len(columns))
        return columns[:_len_], args[:_len_]

    return columns, args
