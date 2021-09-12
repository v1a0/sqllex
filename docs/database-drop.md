# AbstractDatabase.drop


```python
def drop(
        self,
        TABLE: Union[AnyStr, AbstractTable],
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
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER

db: AbstractDatabase = ...

db.create_table('table1', {'id': INTEGER})
db.create_table('table2', {'id': INTEGER})
db.create_table('table3', {'id': INTEGER})

db.drop('table1')
db.drop(TABLE='table2')
db.drop(TABLE='table3', IF_EXIST=True)
db.drop(TABLE='table4', IF_EXIST=True)
```


### [Back to home](README.md)