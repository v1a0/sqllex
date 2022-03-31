# SQLite3x.get_columns

```python
def get_columns(
        self,
        table: AnyStr
) -> Generator[SQLite3xColumn, None, None]:
    """
    Get columns of table as AbstractColumns objects
    
    Parameters
    ----------
    table : AnyStr
        Name of table
    Returns
    ----------
    Tuple
        Columns of table as AbstractColumns objects
    """
```

Get columns of table as AbstractColumns objects


## Example

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

for column in db.get_columns('table1'):
    print(column.name)
```


### [Back to home](README.md)