from pathlib import Path
from typing import Literal, Mapping, Union, List, Tuple, AnyStr
from numbers import Number
from sqlite3 import Connection


class SQLRequest:
    """
    SQL request contains script and values (if necessary)
    """

    def __init__(self, script: AnyStr, values: Tuple = None):
        self.script = script
        self.values = values

    def __str__(self):
        return f"""{{SQLiteScript: script={self.script}, values={self.values}}}"""

    def __eq__(self, other):
        return self.script == other.script and self.values == other.values

    def __bool__(self):
        return bool(self.script)


class SQLStatement:
    """
    SQL request contains SQLRequest
    """

    def __init__(self, request: SQLRequest, path: Union[Path, AnyStr], conn: Connection = None):
        self.request = request
        self.path = path
        self.connection = conn

    def __bool__(self):
        return bool(self.request)


# FOREIGN_KEY const type
ForeignKey = Literal["FOREIGN KEY"]

# Types of data for data types of column
DataType = Literal[
    "TEXT",
    "NUMERIC",
    "INTEGER",
    "REAL",
    "NONE",
    "BLOB",
]


# Types of constants used as keywords for column settings
ConstrainType = Union[
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
ListDataType = List[Union[DataType, ConstrainType, Number]]
ColumnDataType = Union[ListDataType, DataType, AnyStr]
ColumnsType = Mapping[AnyStr, ColumnDataType]

# Type for databases template
DBTemplateType = Union[
    Mapping[
        AnyStr,
        ColumnsType
    ]
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
InsertData = Union[
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
WithType = Mapping[
    AnyStr,
    Union[
        SQLStatement,
        AnyStr
    ]
]

# Type for parameter of WHERE argument
WhereType = Union[
    AnyStr,
    Tuple[NumStr],
    List[Union[NumStr, List[NumStr]]],
    Mapping[AnyStr, Union[SQLStatement, NumStr, List]],
]

# Type for parameter of ORDER BY argument
OrderByType = Union[
    NumStr,
    List,
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
                ConstrainType,
            ]
        ]
    ],
    List[
        Union[
            JoinType,
            NumStr,
            ConstrainType,
        ]
    ],
    Union[
        JoinType,
        NumStr,
        ConstrainType,
    ],
]

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
    'JoinType',
    'JoinArgType',
]
