<div align="center">

# SQLite3x.drop

</div><br>

## About

Method to DROP TABLE (IF EXIST)

```python
def drop(
        self,
        TABLE: AnyStr,
        IF_EXIST: bool = True,
        **kwargs
) -> None:
    """
    DROP TABLE (IF EXIST)

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    IF_EXIST : bool
        Check is table exist (boolean)
    """
```


## Examples

```python

from sqllex import *

db = SQLite3x(
    path='database.db',
    template={
        'table1': {'id': INTEGER},
        'table2': {'id': INTEGER},
        'table3': {'id': INTEGER},
    }
)

db.drop('table1')
db.drop(TABLE='table2')
db.drop(TABLE='table3', IF_EXIST=True)

```


### [Back to home](README.md)