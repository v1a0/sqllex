import typing
from pathlib import Path
from typing import Literal, Mapping, Union, Any, List, AnyStr, TypedDict

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

ListDataType = List[Union[DataType, ConstrainType, AnyStr, int]]
ColumnType = Union[ListDataType, DataType, AnyStr]
TableType = Mapping[AnyStr, ColumnType]
DBTemplateType = Mapping[AnyStr, TableType]

# types for inserting
IntStr = Union[int, AnyStr]
InsertType = Union[
    List[IntStr], Mapping[AnyStr, IntStr], IntStr
]

# Path
PathType = Union[Path, AnyStr]
