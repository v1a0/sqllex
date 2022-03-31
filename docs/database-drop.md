# SQLite3x.drop


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
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table('table1', {'id': sx.INTEGER})
db.create_table('table2', {'id': sx.INTEGER})
db.create_table('table3', {'id': sx.INTEGER})

db.drop('table1')
db.drop(TABLE='table2')
db.drop(TABLE='table3', IF_EXIST=True)
db.drop(TABLE='table4', IF_EXIST=True)
```


### [Back to home](README.md)