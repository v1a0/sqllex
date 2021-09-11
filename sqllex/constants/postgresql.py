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
INTEGER: ColumnDataType = INTEGER
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
REAL: ColumnDataType = REAL
INT2: str = "INT2"
SMALLINT = INT2
SERIAL2: str = "SERIAL2"
SMALLSERIAL = SERIAL2
SERIAL4: str = "SERIAL4"
SERIAL = SERIAL4
TEXT: ColumnDataType = TEXT
# TIME: str =
# TIME: str =
# TIMESTAMP: str =
# TIMESTAMP: str =
TSQUERY: str = "TSQUERY"
TSVECTOR: str = "TSVECTOR"
TXID_SNAPSHOT: str = "TXID_SNAPSHOT"
UUID: str = "UUID"
XML: str = "XML"



