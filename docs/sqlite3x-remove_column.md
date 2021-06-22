# SQLite3x.remove_column

```python
def remove_column(
    self,
    table: AnyStr,
    column: Union[AnyStr, SQLite3xColumn]
):
    """
    Removes column from the table
    
    Parameters
    ----------
    table : AnyStr
        Name of table
    column : Union[AnyStr, SQLite3xColumn]
        Name of column or SQLite3xColumn object.
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
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        'group': [INTEGER, NOT_NULL]
    }
)

print(db.get_columns_names('users'))  # ['id', 'name', 'group']


db.remove_column(
    'users',
    'group'
)

print(db.get_columns_names('users'))  # ['id', 'name']


db.remove_column(
    'users',
    db['users']['name']
)

print(db.get_columns_names('users'))  # ['id']

```


### [Back to home](./index.md)