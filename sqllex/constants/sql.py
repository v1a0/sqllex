from sqllex.types.types import *

# Options of column datatype of value
TEXT: DataType = "TEXT"
NUMERIC: DataType = "NUMERIC"
INTEGER: DataType = "INTEGER"
REAL: DataType = "REAL"
NONE: DataType = "NONE"
BLOB: DataType = "BLOB"


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
AS: ConstrainType = "AS"
ON: ConstrainType = "ON"


# Options for JOIN-ing
INNER_JOIN: JoinType = "INNER JOIN"
LEFT_JOIN: JoinType = "LEFT JOIN"
CROSS_JOIN: JoinType = "CROSS JOIN"


# Options for "OR" argument
ABORT: OrOptionsType = "ABORT"
FAIL: OrOptionsType = "FAIL"
IGNORE: OrOptionsType = "IGNORE"
REPLACE: OrOptionsType = "REPLACE"
ROLLBACK: OrOptionsType = "ROLLBACK"


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


CONSTANTS = [
    TEXT,
    NUMERIC,
    INTEGER,
    REAL,
    NONE,
    BLOB,

    ALL,
    AUTOINCREMENT,
    CHECK,
    DEFAULT,
    FOREIGN_KEY,
    NOT_NULL,
    NULL,
    PRIMARY_KEY,
    REFERENCES,
    UNIQUE,
    AS,
    ON,

    ABORT,
    FAIL,
    IGNORE,
    REPLACE,
    ROLLBACK,
]


__all__ = [
    'ABORT',
    'ALL',
    'AS',
    'AUTOINCREMENT',

    'BLOB',

    'CHECK',
    'CONST_PRIORITY',
    'CROSS_JOIN',

    'DEFAULT',

    'FAIL',
    'FOREIGN_KEY',

    'IGNORE',
    'INNER_JOIN',
    'INTEGER',

    'LEFT_JOIN',

    'NONE',
    'NOT_NULL',
    'NULL',
    'NUMERIC',

    'ON',

    'PRIMARY_KEY',

    'REAL',
    'REFERENCES',
    'REPLACE',
    'ROLLBACK',

    'TEXT',

    'UNIQUE'
]

