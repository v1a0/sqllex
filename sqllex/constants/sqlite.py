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
ABORT: OrOptionsType = "ABORT"
FAIL: OrOptionsType = "FAIL"
IGNORE: OrOptionsType = "IGNORE"
REPLACE: OrOptionsType = "REPLACE"
ROLLBACK: OrOptionsType = "ROLLBACK"


