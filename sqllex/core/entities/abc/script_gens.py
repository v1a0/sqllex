"""
Functions to generate string scripts, like:
"INSERT INTO table_name VALUES (?, ?, ?)"

All functions caching in memory to make it works faster
"""
from functools import lru_cache



@lru_cache(maxsize=32)
def insert_fast(table: str, ph_amount: int, need_space: bool = None, placeholder='?'):
    return f"" \
           f"{' ' if need_space else ''}" \
           f'INTO "{str(table)}" ' \
           f"VALUES (" \
           f"{', '.join((placeholder for _ in range(ph_amount)))})"


@lru_cache(maxsize=32)
def insert_fast_with_prefix(script: str, table: str, ph_amount: int, placeholder: str = '?', need_space: bool = None):
    return f"{script} {insert_fast(table=table, placeholder=placeholder, ph_amount=ph_amount, need_space=need_space)}"


@lru_cache(maxsize=32)
def insert(script: str, table: str, columns: tuple, placeholder='?'):
    return f"" \
           f"{script} " \
           f'INTO "{str(table)}" (' \
           f"{', '.join(col for col in columns)}) " \
           f"VALUES (" \
           f"{', '.join((placeholder for _ in range(len(columns))))})"


@lru_cache(maxsize=32)
def update_script(table: str, script: str):
    return f'{script} UPDATE "{table}" SET '


@lru_cache(maxsize=32)
def select(method: str, columns: tuple, table: str = None):
    return f"" \
           f"{method} "\
           f"{', '.join(str(col) for col in columns)} "\
           f'FROM "{str(table)}" '


@lru_cache(maxsize=32)
def drop(table: str, if_exist: bool = None):
    return f"DROP TABLE " \
           f"{'IF EXISTS' if if_exist else ''}" \
           f' "{table}" '


@lru_cache(maxsize=32)
def delete(script: str, table: str):
    return f'{script} DELETE FROM "{table}" '


@lru_cache(maxsize=32)
def create(temp: str, if_not_exist: bool, name: str, content: str, without_rowid: bool):
    return f"CREATE " \
           f"{temp} " \
           f"TABLE " \
           f"{'IF NOT EXISTS' if if_not_exist else ''} " \
           f'"{name}" ' \
           f" {'(' if content else ''}" \
           f"\n" \
           f"{content}" \
           f"\n" \
           f"{')' if content else ''} " \
           f"{'WITHOUT ROWID' if without_rowid else ''};"


@lru_cache(maxsize=32)
def column(name: str, params: tuple):
    return f""""{name}" {' '.join(str(param) for param in params)},\n"""


@lru_cache(maxsize=32)
def column_with_foreign_key(key: str, table: str, column: str):
    return f"FOREIGN KEY ({key}) REFERENCES {table} ({column}), \n"


@lru_cache(maxsize=32)
def pragma_args(arg):
    return f"PRAGMA {arg}"


@lru_cache(maxsize=32)
def pragma_kwargs(parameter: str, value: str):
    return f"PRAGMA {parameter}={value}"

