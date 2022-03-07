"""
Constants for Any SQL-like DRM
"""
from sqllex.types.types import *

# Options of column datatype of value
INTEGER: ColumnDataType = "INTEGER"
REAL: ColumnDataType = "REAL"
TEXT: ColumnDataType = "TEXT"


# Options for JOIN-ing
INNER_JOIN: JoinMethod = "INNER JOIN"
LEFT_JOIN: JoinMethod = "LEFT JOIN"


# Options of column value
ALL: ConstantType = "*"
FOREIGN_KEY: ForeignKey = "FOREIGN KEY"
NULL: ConstantType = "NULL"
PRIMARY_KEY: ConstantType = "PRIMARY KEY"
REFERENCES: ConstantType = "REFERENCES"
AS: ConstantType = "AS"
ON: ConstantType = "ON"
LIKE: ConstantType = "LIKE"


# Options for "OR" argument
ABORT: OrOptionsType = "ABORT"
FAIL: OrOptionsType = "FAIL"
IGNORE: OrOptionsType = "IGNORE"
REPLACE: OrOptionsType = "REPLACE"
ROLLBACK: OrOptionsType = "ROLLBACK"

__all__ = [
    # Options of column datatype of value
    'INTEGER',
    'REAL',
    'TEXT',

    # Options for JOIN-ing
    'INNER_JOIN',
    'LEFT_JOIN',

    # Options of column value
    'ALL',
    'FOREIGN_KEY',
    'NULL',
    'PRIMARY_KEY',
    'REFERENCES',
    'AS',
    'ON',
    'LIKE',

    # Options for "OR" argument
    'ABORT',
    'FAIL',
    'IGNORE',
    'REPLACE',
    'ROLLBACK',
]
