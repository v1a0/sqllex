from typing import Any, AnyStr, Generator, List, Literal, Mapping, Tuple, Union, Iterable, Sized
from pathlib import Path
from numbers import Number

# FOREIGN_KEY const type
ForeignKey = Literal["FOREIGN KEY"]

# Types of data for data types of column
ColumnDataType = Literal[
    "TEXT",
    "NUMERIC",
    "INTEGER",
    "REAL",
    "NONE",
    "BLOB",
]

# Types of constants used as keywords for column settings
ConstantType = Union[
    Literal[
        "*",
        "NOT NULL",
        "DEFAULT",
        "UNIQUE",
        "CHECK",
        "AUTOINCREMENT",
        "PRIMARY KEY",
        "REFERENCES",
        "WITH",
        "OR",
        "NULL",
        "AS",
        "ON",
        "LIKE"
    ],
    ForeignKey
]

# Subtypes for DBTemplateType
ColumnType = Union[
    Tuple[ColumnDataType, ConstantType, str, Number],
    List[Union[ColumnDataType, ConstantType, str, Number]],
    ColumnDataType,
    ConstantType,
    str
]
ColumnsType = Mapping[str, ColumnType]

# Type for databases template
DBTemplateType = Mapping[
    str,
    ColumnsType
]

# Universal Path type
PathType = Union[
    Path,
    str
]

# Type for string or numeric data
NumStr = Union[
    Number,
    str
]

# Type of data INSERT awaiting
InsertingData = Union[
    NumStr,
    tuple,
    list,
    Mapping
]

InsertingManyData = Union[
    List[InsertingData],
    Tuple[InsertingData],
    list, tuple
]

# Type for parameter of OR argument in INSERT method (?)
OrOptionsType = Literal[
    "ABORT",
    "FAIL",
    "IGNORE",
    "REPLACE",
    "ROLLBACK"
]

# Type for parameter of WITH argument
WithType = Mapping[str, str]

# Type for parameter of WHERE argument
WhereType = Union[
    str,
    Mapping,
    bool,    # temporary fix
]

# Type for parameter of ORDER BY argument
OrderByType = Union[
    int,
    str,
    tuple,
    list,
    Mapping[
        str,
        Union[
            str,
            list,
            tuple,
            Number,
        ]
    ]
]

# Type for parameter of LIMIT argument
LimitOffsetType = Union[
    Number,
    str,
]

# Type for parameter of JOIN argument
JoinMethod = Literal[
    "INNER JOIN",
    "LEFT JOIN",
    "CROSS JOIN"
]


JoinArgType = Union[
    Tuple[tuple],
    tuple,
    str
]

ScriptAndValues = Tuple[
    str, tuple
]

GroupByType = Union[
    str, int, tuple, list,
]

__all__ = [
    # sql
    'ForeignKey',
    'ColumnDataType',
    'ConstantType',
    'ColumnType',
    'ColumnsType',
    'DBTemplateType',
    'PathType',
    'Number',
    'NumStr',
    'InsertingData',
    'InsertingManyData',
    'OrOptionsType',
    'WithType',
    'WhereType',
    'OrderByType',
    'LimitOffsetType',
    'JoinMethod',
    'JoinArgType',
    'GroupByType',

    # typing
    'Literal',
    'Mapping',
    'ScriptAndValues',
    'Union',
    'List',
    'AnyStr',
    'Any',
    'Tuple',
    'Generator',
    'Iterable',
    'Sized',
    'JoinMethod',
]
