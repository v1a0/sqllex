from init_types import DataType, ConstrainType

# Const vars
TEXT: DataType = "TEXT"
NUMERIC: DataType = "NUMERIC"
INTEGER: DataType = "INTEGER"
REAL: DataType = "REAL"
NONE: DataType = "NONE"

NOT_NULL: ConstrainType = "NOT NULL"
DEFAULT: ConstrainType = "DEFAULT"
UNIQUE: ConstrainType = "UNIQUE"
PRIMARY_KEY: ConstrainType = "PRIMARY KEY"
CHECK: ConstrainType = "CHECK"
AUTOINCREMENT: ConstrainType = "AUTOINCREMENT"
FOREIGN_KEY: ConstrainType = "FOREIGN KEY"
REFERENCES: ConstrainType = "REFERENCES"

CONSTANTS = [
    TEXT, NUMERIC, INTEGER, REAL, NONE,
    NOT_NULL, DEFAULT, UNIQUE, PRIMARY_KEY, CHECK,
    AUTOINCREMENT, FOREIGN_KEY, REFERENCES
]