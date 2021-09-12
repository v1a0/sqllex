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
    Tuple[ColumnDataType, ConstantType, AnyStr, Number],
    List[Union[ColumnDataType, ConstantType, AnyStr, Number]],
    ColumnDataType,
    ConstantType,
    AnyStr
]
ColumnsType = Mapping[AnyStr, ColumnType]

# Type for databases template
DBTemplateType = Mapping[
    AnyStr,
    ColumnsType
]

# Universal Path type
PathType = Union[
    Path,
    AnyStr
]

# Type for string or numeric data
NumStr = Union[
    Number,
    AnyStr
]

# Type of data INSERT awaiting
InsertingData = Union[
    NumStr,
    Tuple,
    List,
    Mapping
]

InsertingManyData = Union[
    List[InsertingData],
    Tuple[InsertingData],
    List, Tuple
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
WithType = Mapping[AnyStr, AnyStr]

# Type for parameter of WHERE argument
WhereType = Union[
    AnyStr,
    Mapping[AnyStr, Union[NumStr, List]],
    bool,    # temporary fix
]

# Type for parameter of ORDER BY argument
OrderByType = Union[
    NumStr,
    Tuple,
    Mapping[
        AnyStr,
        Union[
            AnyStr,
            Number,
            List,
            Tuple
        ]
    ]
]

# Type for parameter of LIMIT argument
LimitOffsetType = Union[
    Number,
    AnyStr,
]

# Type for parameter of JOIN argument
JoinMethod = Literal[
    "INNER JOIN",
    "LEFT JOIN",
    "CROSS JOIN"
]


JoinArgType = Union[
    Tuple[
        Tuple[
            Union[
                JoinMethod,
                NumStr,
                ConstantType,
            ]
        ]
    ],
    Tuple[
        Union[
            JoinMethod,
            NumStr,
            ConstantType,
            AnyStr
        ]
    ],
    AnyStr
]

ScriptAndValues = Tuple[
    AnyStr, Tuple
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
