from functools import lru_cache

"""
Functions to generate string scripts, like:
"INSERT INTO table_name VALUES (?, ?, ?)"

All functions caching in memory to make it works faster
"""


@lru_cache(maxsize=32)
def pragma_args(arg):
    return f"PRAGMA {arg}"


@lru_cache(maxsize=32)
def pragma_kwargs(parameter: str, value: str):
    return f"PRAGMA {parameter}={value}"

