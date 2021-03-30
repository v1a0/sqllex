from sqllex.types_.types import *

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
FOREIGN_KEY: KeyType = "FOREIGN KEY"
REFERENCES: ConstrainType = "REFERENCES"

ABORT: InsertOrOptions = "ABORT"
FAIL: InsertOrOptions = "FAIL"
IGNORE: InsertOrOptions = "IGNORE"
REPLACE: InsertOrOptions = "REPLACE"
ROLLBACK: InsertOrOptions = "ROLLBACK"


CONSTANTS = [
    TEXT, NUMERIC, INTEGER, REAL, NONE,
    NOT_NULL, DEFAULT, UNIQUE, PRIMARY_KEY, CHECK,
    AUTOINCREMENT, FOREIGN_KEY, REFERENCES, ABORT, FAIL, IGNORE, REPLACE, ROLLBACK
]