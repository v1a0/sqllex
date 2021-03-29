from pathlib import Path
from typing import Literal, Mapping, Union, List, AnyStr, Any, MutableMapping
from numbers import Number

KeyType = Literal["FOREIGN KEY"]
DataType = Literal["TEXT", "NUMERIC", "INTEGER", "REAL", "NONE"]

ConstrainType = Union[
    Literal["NOT NULL", "DEFAULT", "UNIQUE", "CHECK", "AUTOINCREMENT", "PRIMARY KEY", "REFERENCES", "WITH"],
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


class ScriptValues:
    def __init__(self, script: str, values: tuple):
        self.script = script
        self.values = values

    def __str__(self):
        return f"""{{SQLiteScript: script={self.script}, values={self.values}}}"""


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
        ScriptValues
    ]
