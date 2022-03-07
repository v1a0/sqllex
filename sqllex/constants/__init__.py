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
    # Options of column datatype of value
    # sql
    'INTEGER',  # lgtm [py/undefined-export]
    'REAL',  # lgtm [py/undefined-export]
    'TEXT',  # lgtm [py/undefined-export]
    # sqlite
    'NUMERIC',  # lgtm [py/undefined-export]
    'NONE',  # lgtm [py/undefined-export]
    'BLOB',  # lgtm [py/undefined-export]
    # psql
    'INT8',  # lgtm [py/undefined-export]
    'SERIAL8',  # lgtm [py/undefined-export]
    'BIGSERIAL',  # lgtm [py/undefined-export]
    'BOOL',  # lgtm [py/undefined-export]
    'BOOLEAN',  # lgtm [py/undefined-export]
    'BOX',  # lgtm [py/undefined-export]
    'BYTEA',  # lgtm [py/undefined-export]
    'CIDR',  # lgtm [py/undefined-export]
    'CIRCLE',  # lgtm [py/undefined-export]
    'DATE',  # lgtm [py/undefined-export]
    'FLOAT8',  # lgtm [py/undefined-export]
    'INET',  # lgtm [py/undefined-export]
    'INT',  # lgtm [py/undefined-export]
    'INT4',  # lgtm [py/undefined-export]
    'JSON',  # lgtm [py/undefined-export]
    'JSONB',  # lgtm [py/undefined-export]
    'LINE',  # lgtm [py/undefined-export]
    'LSEG',  # lgtm [py/undefined-export]
    'MACADDR',  # lgtm [py/undefined-export]
    'MACADDR8',  # lgtm [py/undefined-export]
    'MONEY',  # lgtm [py/undefined-export]
    'PATH',  # lgtm [py/undefined-export]
    'PG_LSN',  # lgtm [py/undefined-export]
    'POINT',  # lgtm [py/undefined-export]
    'POLYGON',  # lgtm [py/undefined-export]
    'FLOAT4',  # lgtm [py/undefined-export]
    'INT2',  # lgtm [py/undefined-export]
    'SMALLINT',  # lgtm [py/undefined-export]
    'SERIAL2',  # lgtm [py/undefined-export]
    'SMALLSERIAL',  # lgtm [py/undefined-export]
    'SERIAL4',  # lgtm [py/undefined-export]
    'SERIAL',  # lgtm [py/undefined-export]
    'TSQUERY',  # lgtm [py/undefined-export]
    'TSVECTOR',  # lgtm [py/undefined-export]
    'TXID_SNAPSHOT',  # lgtm [py/undefined-export]
    'UUID',  # lgtm [py/undefined-export]
    'XML',  # lgtm [py/undefined-export]


    # Options for JOIN-ing
    'INNER_JOIN',  # lgtm [py/undefined-export]
    'LEFT_JOIN',  # lgtm [py/undefined-export]
    # sqlite
    'CROSS_JOIN',  # lgtm [py/undefined-export]
    # psql
    # None


    # Options of column value
    'ALL',  # lgtm [py/undefined-export]
    'FOREIGN_KEY',  # lgtm [py/undefined-export]
    'NULL',  # lgtm [py/undefined-export]
    'PRIMARY_KEY',  # lgtm [py/undefined-export]
    'REFERENCES',  # lgtm [py/undefined-export]
    'AS',  # lgtm [py/undefined-export]
    'ON',  # lgtm [py/undefined-export]
    'LIKE',  # lgtm [py/undefined-export]
    # sqlite
    'AUTOINCREMENT',  # lgtm [py/undefined-export]
    'CHECK',  # lgtm [py/undefined-export]
    'DEFAULT',  # lgtm [py/undefined-export]
    'NOT_NULL',  # lgtm [py/undefined-export]
    'UNIQUE',  # lgtm [py/undefined-export]
    # psql
    # None


    # Options for "OR" argument
    'ABORT',  # lgtm [py/undefined-export]
    'FAIL',  # lgtm [py/undefined-export]
    'IGNORE',  # lgtm [py/undefined-export]
    'REPLACE',  # lgtm [py/undefined-export]
    'ROLLBACK',  # lgtm [py/undefined-export]
    # sqlite
    # None
    # psql
    # None
]
