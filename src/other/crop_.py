from loguru import logger
from typing import Union


def crop(columns: Union[tuple, list], args: Union[tuple, list]) -> tuple:
    if args and columns:
        if len(args) != len(columns):
            logger.warning(f"SIZE CROP! Expecting {len(columns)} arguments but {len(args)} were given!")
            _len_ = min(len(args), len(columns))
            return columns[:_len_], args[:_len_]

    return columns, args
