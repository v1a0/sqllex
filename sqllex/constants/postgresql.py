"""
Constants for PostgreSQL
"""
from sqllex.constants.sql import *
from sqllex.types.types import *

# Options of column datatype of value
INT8: str = "INT8"
BIGINT = INT8
SERIAL8: str = "SERIAL8"
BIGSERIAL = SERIAL8
# BIT: str =
# VARBIT: str =
BOOL: str = "BOOL"
BOOLEAN = BOOL
BOX: str = "BOX"
BYTEA: str = "BYTEA"
CIDR: str = "CIDR"
CIRCLE: str = "CIRCLE"
DATE: str = "DATE"
FLOAT8: str = "FLOAT8"
INET: str = "INET"
INT: str = "INT"
INT4: str = "INT4"
# INTEGER: ColumnDataType = INTEGER
# INTERVAL: str =
JSON: str = "JSON"
JSONB: str = "JSONB"
LINE: str = "LINE"
LSEG: str = "LSEG"
MACADDR: str = "MACADDR"
MACADDR8: str = "MACADDR8"
MONEY: str = "MONEY"
# NUMERIC: str =
PATH: str = "PATH"
PG_LSN: str = "PG_LSN"
POINT: str = "POINT"
POLYGON: str = "POLYGON"
FLOAT4: str = "FLOAT4"
# REAL: ColumnDataType = REAL
INT2: str = "INT2"
SMALLINT = INT2
SERIAL2: str = "SERIAL2"
SMALLSERIAL = SERIAL2
SERIAL4: str = "SERIAL4"
SERIAL = SERIAL4
# TEXT: ColumnDataType = TEXT
# TIME: str =
# TIME: str =
# TIMESTAMP: str =
# TIMESTAMP: str =
TSQUERY: str = "TSQUERY"
TSVECTOR: str = "TSVECTOR"
TXID_SNAPSHOT: str = "TXID_SNAPSHOT"
UUID: str = "UUID"
XML: str = "XML"

__all__ = [
    # Options of column datatype of value
    'INTEGER',  # lgtm [py/undefined-export]
    'REAL',  # lgtm [py/undefined-export]
    'TEXT',  # lgtm [py/undefined-export]
    'INT8',
    'SERIAL8',
    'BIGSERIAL',
    'BOOL',
    'BOOLEAN',
    'BOX',
    'BYTEA',
    'CIDR',
    'CIRCLE',
    'DATE',
    'FLOAT8',
    'INET',
    'INT',
    'INT4',
    'JSON',
    'JSONB',
    'LINE',
    'LSEG',
    'MACADDR',
    'MACADDR8',
    'MONEY',
    'PATH',
    'PG_LSN',
    'POINT',
    'POLYGON',
    'FLOAT4',
    'INT2',
    'SMALLINT',
    'SERIAL2',
    'SMALLSERIAL',
    'SERIAL4',
    'SERIAL',
    'TSQUERY',
    'TSVECTOR',
    'TXID_SNAPSHOT',
    'UUID',
    'XML',

    # Options for JOIN-ing
    'INNER_JOIN',  # lgtm [py/undefined-export]
    'LEFT_JOIN',  # lgtm [py/undefined-export]

    # Options of column value
    'ALL',  # lgtm [py/undefined-export]
    'FOREIGN_KEY',  # lgtm [py/undefined-export]
    'NULL',  # lgtm [py/undefined-export]
    'PRIMARY_KEY',  # lgtm [py/undefined-export]
    'REFERENCES',  # lgtm [py/undefined-export]
    'AS',  # lgtm [py/undefined-export]
    'ON',  # lgtm [py/undefined-export]
    'LIKE',  # lgtm [py/undefined-export]

    # Options for "OR" argument
    'ABORT',  # lgtm [py/undefined-export]
    'FAIL',  # lgtm [py/undefined-export]
    'IGNORE',  # lgtm [py/undefined-export]
    'REPLACE',  # lgtm [py/undefined-export]
    'ROLLBACK',  # lgtm [py/undefined-export]
]
