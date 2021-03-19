from pathlib import Path
from typing import Literal, Mapping, Union, List, AnyStr, Any
from numbers import Number

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


# Path
PathType = Union[Path, AnyStr]

# Other
NumStr = Union[Number, AnyStr]

if __name__ == "__main__":
    __all__ = [
        KeyType,
        DataType,
        ConstrainType,

        ListDataType,
        ColumnType,
        TableType,
        DBTemplateType,

        PathType,
        NumStr,
    ]
