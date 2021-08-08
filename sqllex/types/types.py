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
        "ON"
    ],
    ForeignKey
]

# Subtypes for DBTemplateType
ColumnType = Union[
    Tuple[ColumnDataType, ConstantType, AnyStr, Number],
    List[Union[ColumnDataType, ConstantType, AnyStr, Number]],
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
JoinType = Union[
    Literal[
        "INNER JOIN",
        "LEFT JOIN",
        "CROSS JOIN"
    ],
]

JoinArgType = Union[
    List[
        List[
            Union[
                JoinType,
                NumStr,
                ConstantType,
            ]
        ]
    ],
    List[
        Union[
            JoinType,
            NumStr,
            ConstantType,
        ]
    ],
    Tuple[
        Tuple[
            Union[
                JoinType,
                NumStr,
                ConstantType,
            ]
        ]
    ],
    Tuple[
        Union[
            JoinType,
            NumStr,
            ConstantType,
        ]
    ],
    Union[
        JoinType,
        NumStr,
        ConstantType,
    ],
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
    'OrOptionsType',
    'WithType',
    'WhereType',
    'OrderByType',
    'LimitOffsetType',
    'JoinType',
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
]
