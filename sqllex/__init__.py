"""
Sqllex package
"""
from sqllex.classes import *
from sqllex.constants import *
from sqllex.debug import logger

print("""
\t\t\t\33[41m!!!\tWARNING\t!!!\033[0m
\033[91m
SQLLEX v0.2 have major changes that may breaks your old code! 
Please, read https://github.com/v1a0/sqllex/blob/main/UPDATES.md#0200
if you are moving from v0.1.10.5 to v0.2+, and open an issue if you have any bugs.
\033[0m\33[93m
Thanks for you support and feedback!\033[0m""")

__version__ = '0.2.0.1a'

__all__ = [
    # classes
    # SQLite3x
    "SQLite3x",                     # lgtm [py/undefined-export]
    # "SQLite3xTable",              # lgtm [py/undefined-export]
    # "AbstractColumn",             # lgtm [py/undefined-export]
    # "SQLite3xSearchCondition",    # lgtm [py/undefined-export]

    # PostgreSQL
    "PostgreSQLx",                  # lgtm [py/undefined-export]
    # "PostgreSQLxTable",           # lgtm [py/undefined-export]

    # constants
    "TEXT",                         # lgtm [py/undefined-export]
    "NUMERIC",                      # lgtm [py/undefined-export]
    "INTEGER",                      # lgtm [py/undefined-export]
    "REAL",                         # lgtm [py/undefined-export]
    "NONE",                         # lgtm [py/undefined-export]
    "BLOB",                         # lgtm [py/undefined-export]
    "NOT_NULL",                     # lgtm [py/undefined-export]
    "DEFAULT",                      # lgtm [py/undefined-export]
    "UNIQUE",                       # lgtm [py/undefined-export]
    "PRIMARY_KEY",                  # lgtm [py/undefined-export]
    "CHECK",                        # lgtm [py/undefined-export]
    "AUTOINCREMENT",                # lgtm [py/undefined-export]
    "FOREIGN_KEY",                  # lgtm [py/undefined-export]
    "REFERENCES",                   # lgtm [py/undefined-export]
    "ABORT",                        # lgtm [py/undefined-export]
    "FAIL",                         # lgtm [py/undefined-export]
    "IGNORE",                       # lgtm [py/undefined-export]
    "REPLACE",                      # lgtm [py/undefined-export]
    "ROLLBACK",                     # lgtm [py/undefined-export]
    "NULL",                         # lgtm [py/undefined-export]
    "AS",                           # lgtm [py/undefined-export]
    "ON",                           # lgtm [py/undefined-export]
    "ALL",                          # lgtm [py/undefined-export]
    "INNER_JOIN",                   # lgtm [py/undefined-export]
    "LEFT_JOIN",                    # lgtm [py/undefined-export]
    "CROSS_JOIN",                   # lgtm [py/undefined-export]
    "LIKE",                         # lgtm [py/undefined-export]

    # debug tools
    "logger",                       # lgtm [py/undefined-export]
]
