# AbstractDatabase.get_columns_names


```python
def get_columns_names(
        self,
        table: AnyStr
) -> List[str]:
    """
    Get list of names of table columns as strings
    
    Parameters
    ----------
    table : AnyStr
        Name of table
    Returns
    ----------
    List[List]
        Columns of table
    """
```


## Example

```python
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

for column_name in db.get_columns_names('table1'):
    print(column_name)
```

### [Back to home](README.md)