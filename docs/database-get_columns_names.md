# SQLite3x.get_columns_names


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
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

for column_name in db.get_columns_names('table1'):
    print(column_name)
```

### [Back to home](README.md)