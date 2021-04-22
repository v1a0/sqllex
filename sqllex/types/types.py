from pathlib import Path
from typing import Literal, Mapping, Union, List, Tuple, AnyStr
from numbers import Number


class SQLRequest:
    """
    SQL request contains script and values (if necessary)
    """

    def __init__(self, script: str, values: tuple = None):
        self.script = script
        self.values = values

    def __str__(self):
        return f"""{{SQLiteScript: script={self.script}, values={self.values}}}"""

    def __eq__(self, other):
        return self.script == other.script and self.values == other.values


class SQLStatement:
    """
    SQL request contains SQLRequest
    """

    def __init__(self, request: SQLRequest, path: Union[Path, AnyStr]):
        self.request = request
        self.path = path


# FOREIGN_KEY const type
ForeignKey = Literal["FOREIGN KEY"]

# Types of data for data types of column
DataType = Literal["TEXT", "NUMERIC", "INTEGER", "REAL", "NONE", "BLOB"]

# Types of constants used as keywords for column settings
ConstrainType = Union[
    Literal[
        "*", "NOT NULL", "DEFAULT", "UNIQUE", "CHECK", "AUTOINCREMENT",
        "PRIMARY KEY", "REFERENCES", "WITH", "OR", "NULL"
    ],
    ForeignKey
]

# Subtypes for DBTemplateType
ListDataType = List[Union[DataType, ConstrainType, Number]]
ColumnDataType = Union[ListDataType, DataType, AnyStr]
ColumnsType = Mapping[AnyStr, ColumnDataType]

# Type for databases template
DBTemplateType = Mapping[AnyStr, ColumnsType]

# Universal Path type
PathType = Union[Path, AnyStr]

# Type for string or numeric data
NumStr = Union[Number, AnyStr]

# Type of data INSERT awaiting
InsertData = Union[NumStr, tuple, List, Mapping]

# Type for parameter of OR argument in INSERT method (?)
OrOptionsType = Literal["ABORT", "FAIL", "IGNORE", "REPLACE", "ROLLBACK"]

# Type for parameter of WITH argument
WithType = Mapping[str, Union[SQLStatement, str]]

# Type for parameter of WITH argument
WhereType = Union[
    AnyStr,
    Tuple[NumStr], List[Union[NumStr, List[NumStr]]],
    Mapping[str, Union[SQLStatement, NumStr]]
]

# Type for parameter of ORDER BY argument
OrderByType = Union[int, str, list, tuple, Mapping[str, Union[str, int, list, tuple]]]

# Type for parameter of LIMIT argument
LimitOffsetType = Union[int, str, float]


__all__ = [
    'SQLRequest',
    'SQLStatement',
    'ForeignKey',
    'DataType',
    'ConstrainType',
    'ListDataType',
    'ColumnDataType',
    'ColumnsType',
    'DBTemplateType',
    'PathType',
    'NumStr',
    'InsertData',
    'OrOptionsType',
    'WithType',
    'WhereType',
    'OrderByType',
    'LimitOffsetType',
]
