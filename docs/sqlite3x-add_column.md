# SQLite3x.add_column

```python
def add_column(
    self,
    table: AnyStr,
    column: ColumnDataType
) -> None:
    """
    Adds column to the table
    Parameters
    ----------
    table : AnyStr
        Name of table
    column : ColumnDataType
        Columns of table (ColumnsType-like)
        Column name and SQL type e.g. {'value': INTEGER}
    Returns
    ----------
    None
    """
```

# Examples

```python
from sqllex import *

db = SQLite3x(path='database.db')

db.create_table(
    'users',
    {
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
    }
)

print(db.get_columns_names('users'))  # ['id', 'name']

db.add_column(
    'users', 
    {
        'group': [INTEGER, NOT_NULL]
    },
)

print(db.get_columns_names('users'))  # ['id', 'name', 'group']

```

### [Back to home](README.md)