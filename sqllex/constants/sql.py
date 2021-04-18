from sqllex.types.types import *

# Options of column datatype of value
TEXT: DataType = "TEXT"
NUMERIC: DataType = "NUMERIC"
INTEGER: DataType = "INTEGER"
REAL: DataType = "REAL"
NONE: DataType = "NONE"


# Options of column value
ALL: ConstrainType = "*"
AUTOINCREMENT: ConstrainType = "AUTOINCREMENT"
CHECK: ConstrainType = "CHECK"
DEFAULT: ConstrainType = "DEFAULT"
FOREIGN_KEY: ForeignKey = "FOREIGN KEY"
NOT_NULL: ConstrainType = "NOT NULL"
NULL: ConstrainType = "NULL"
PRIMARY_KEY: ConstrainType = "PRIMARY KEY"
REFERENCES: ConstrainType = "REFERENCES"
UNIQUE: ConstrainType = "UNIQUE"


# Options for "OR" argument
ABORT: OrOptionsType = "ABORT"
FAIL: OrOptionsType = "FAIL"
IGNORE: OrOptionsType = "IGNORE"
REPLACE: OrOptionsType = "REPLACE"
ROLLBACK: OrOptionsType = "ROLLBACK"


CONSTANTS = [
    ALL, TEXT, NUMERIC, INTEGER, REAL, NONE,
    NOT_NULL, DEFAULT, UNIQUE, PRIMARY_KEY, CHECK,
    AUTOINCREMENT, FOREIGN_KEY, REFERENCES, ABORT,
    FAIL, IGNORE, REPLACE, ROLLBACK, NULL
]

__all__ = [
    "ALL",
    "TEXT",
    "NUMERIC",
    "INTEGER",
    "REAL",
    "NONE",
    "NOT_NULL",
    "DEFAULT",
    "UNIQUE",
    "PRIMARY_KEY",
    "CHECK",
    "AUTOINCREMENT",
    "FOREIGN_KEY",
    "REFERENCES",
    "ABORT",
    "FAIL",
    "IGNORE",
    "REPLACE",
    "ROLLBACK",
    "NULL",
]
