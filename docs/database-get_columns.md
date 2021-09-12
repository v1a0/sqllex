# AbstractDatabase.get_columns

```python
def get_columns(
        self,
        table: AnyStr
) -> Generator[AbstractColumn, None, None]:
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
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

for column in db.get_columns('table1'):
    print(column.name)
```


### [Back to home](README.md)