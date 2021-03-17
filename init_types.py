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

my_template: TemplateType = {
    "my_table": {
        "id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, DEFAULT, '1337'],
        "age": INTEGER
    }
}
"""
DataType = Literal["TEXT", "NUMERIC", "INTEGER", "REAL", "NONE"]
ConstrainType = Literal[
    "NOT NULL", "DEFAULT", "UNIQUE",
    "CHECK", "AUTOINCREMENT",
    "PRIMARY KEY", "FOREIGN KEY", "REFERENCES",
]
MultipleDataType = List[Union[DataType, ConstrainType, AnyStr, int]]
ColumnType = Union[MultipleDataType, DataType, AnyStr]
TableType = Mapping[AnyStr, ColumnType]
TemplateType = Mapping[AnyStr, TableType]

# types for inserting
IntStr = Union[int, AnyStr]
InsertType = Union[
    List[IntStr], Mapping[AnyStr, IntStr], IntStr
]

# Path
PathType = Union[Path, AnyStr]