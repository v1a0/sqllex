"""
All constants, SQL aliases of different DMS (sqlite, postgres, common)
"""

from sqllex.constants.sqlite import *
from sqllex.constants.postgresql import *


CONST_PRIORITY = {
    TEXT: 0,
    NUMERIC: 0,
    INTEGER: 0,
    REAL: 0,
    NONE: 1,
    BLOB: 0,

    ALL: None,
    AUTOINCREMENT: 2,
    CHECK: None,
    DEFAULT: 1,
    FOREIGN_KEY: None,
    NOT_NULL: 3,
    NULL: 1,
    PRIMARY_KEY: 1,
    REFERENCES: None,
    UNIQUE: 1,
    AS: None,
    ON: None,

    ABORT: None,
    FAIL: None,
    IGNORE: None,
    REPLACE: None,
    ROLLBACK: None,
}

CONST_PRIORITY.setdefault(1)


__all__ = [
    # sql
    'ABORT',  # lgtm [py/undefined-export]
    'ALL',  # lgtm [py/undefined-export]
    'AS',  # lgtm [py/undefined-export]
    'AUTOINCREMENT',  # lgtm [py/undefined-export]

    'BLOB',  # lgtm [py/undefined-export]

    'CHECK',  # lgtm [py/undefined-export]
    'CONST_PRIORITY',  # lgtm [py/undefined-export]
    'CROSS_JOIN',  # lgtm [py/undefined-export]

    'DEFAULT',  # lgtm [py/undefined-export]

    'FAIL',  # lgtm [py/undefined-export]
    'FOREIGN_KEY',  # lgtm [py/undefined-export]

    'IGNORE',  # lgtm [py/undefined-export]
    'INNER_JOIN',  # lgtm [py/undefined-export]
    'INTEGER',  # lgtm [py/undefined-export]

    'LEFT_JOIN',  # lgtm [py/undefined-export]
    'LIKE',  # lgtm [py/undefined-export]

    'NONE',  # lgtm [py/undefined-export]
    'NOT_NULL',  # lgtm [py/undefined-export]
    'NULL',  # lgtm [py/undefined-export]
    'NUMERIC',  # lgtm [py/undefined-export]

    'ON',  # lgtm [py/undefined-export]

    'PRIMARY_KEY',  # lgtm [py/undefined-export]

    'REAL',  # lgtm [py/undefined-export]
    'REFERENCES',  # lgtm [py/undefined-export]
    'REPLACE',  # lgtm [py/undefined-export]
    'ROLLBACK',  # lgtm [py/undefined-export]

    'TEXT',  # lgtm [py/undefined-export]

    'UNIQUE'  # lgtm [py/undefined-export]
]
