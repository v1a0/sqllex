import typing
from pathlib import Path
from typing import Literal, Mapping, Union, Any, List, AnyStr, TypedDict
from numbers import Number

ReadOnlyMode = Literal["r", "r+"]
WriteAndTruncateMode = Literal["w", "w+", "wt", "w+t"]
WriteNoTruncateMode = Literal["r+", "r+t"]
AppendMode = Literal["a", "a+", "at", "a+t"]
ReadType = Literal[ReadOnlyMode, WriteAndTruncateMode, WriteNoTruncateMode, AppendMode]

"""
Types for db init-on from template

db_template: DBTemplateType = {
    "my_table": {
        "id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, DEFAULT, '1337'],
        "age": INTEGER
    }
}
"""

KeyType = Literal["FOREIGN KEY"]
DataType = Literal["TEXT", "NUMERIC", "INTEGER", "REAL", "NONE"]

ConstrainType = Union[
    Literal["NOT NULL", "DEFAULT", "UNIQUE", "CHECK", "AUTOINCREMENT", "PRIMARY KEY", "REFERENCES"],
    KeyType
]

ListDataType = List[Union[DataType, ConstrainType, AnyStr, Number]]
ColumnType = Union[ListDataType, DataType, AnyStr]
TableType = Mapping[AnyStr, ColumnType]
DBTemplateType = Mapping[AnyStr, TableType]

# types for inserting
NumStr = Union[Number, AnyStr]
InsertArgs = Union[
    List[NumStr], NumStr, Mapping
]
InsertKwargs = Mapping[AnyStr, NumStr]

# Path
PathType = Union[Path, AnyStr]
