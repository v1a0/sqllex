"""
Constants for SQLite
"""
from sqllex.types.types import *
from sqllex.constants.sql import *


# Options of column datatype of value
# TEXT: ColumnDataType = "TEXT"
NUMERIC: ColumnDataType = "NUMERIC"
# INTEGER: ColumnDataType = "INTEGER"
# REAL: ColumnDataType = "REAL"
NONE: ColumnDataType = "NONE"
BLOB: ColumnDataType = "BLOB"


# Options for JOIN-ing
# INNER_JOIN: JoinMethod = "INNER JOIN"
# LEFT_JOIN: JoinMethod = "LEFT JOIN"
CROSS_JOIN: JoinMethod = "CROSS JOIN"


# Options of column value
# ALL: ConstantType = "*"
AUTOINCREMENT: ConstantType = "AUTOINCREMENT"
CHECK: ConstantType = "CHECK"
DEFAULT: ConstantType = "DEFAULT"
# FOREIGN_KEY: ForeignKey = "FOREIGN KEY"
NOT_NULL: ConstantType = "NOT NULL"
# NULL: ConstantType = "NULL"
# PRIMARY_KEY: ConstantType = "PRIMARY KEY"
# REFERENCES: ConstantType = "REFERENCES"
UNIQUE: ConstantType = "UNIQUE"
# AS: ConstantType = "AS"
# ON: ConstantType = "ON"



# Options for "OR" argument
# ABORT: OrOptionsType = "ABORT"
# FAIL: OrOptionsType = "FAIL"
# IGNORE: OrOptionsType = "IGNORE"
# REPLACE: OrOptionsType = "REPLACE"
# ROLLBACK: OrOptionsType = "ROLLBACK"


__all__ = [
    # Options of column datatype of value
    'INTEGER',  # lgtm [py/undefined-export]
    'REAL',  # lgtm [py/undefined-export]
    'TEXT',  # lgtm [py/undefined-export]
    'NUMERIC',
    'NONE',
    'BLOB',

    # psql


    # Options for JOIN-ing
    'INNER_JOIN',  # lgtm [py/undefined-export]
    'LEFT_JOIN',  # lgtm [py/undefined-export]
    'CROSS_JOIN',

    # Options of column value
    'ALL',  # lgtm [py/undefined-export]
    'FOREIGN_KEY',  # lgtm [py/undefined-export]
    'NULL',  # lgtm [py/undefined-export]
    'PRIMARY_KEY',  # lgtm [py/undefined-export]
    'REFERENCES',  # lgtm [py/undefined-export]
    'AS',  # lgtm [py/undefined-export]
    'ON',  # lgtm [py/undefined-export]
    'LIKE',  # lgtm [py/undefined-export]
    'AUTOINCREMENT',
    'CHECK',
    'DEFAULT',
    'NOT_NULL',
    'UNIQUE',

    # Options for "OR" argument
    'ABORT',  # lgtm [py/undefined-export]
    'FAIL',  # lgtm [py/undefined-export]
    'IGNORE',  # lgtm [py/undefined-export]
    'REPLACE',  # lgtm [py/undefined-export]
    'ROLLBACK',  # lgtm [py/undefined-export]
]
