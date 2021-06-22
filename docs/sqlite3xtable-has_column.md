# SQLite3xTable.has_column

```python
def has_column(self, column: Union[AnyStr, SQLite3xColumn]) -> bool:
    """
    Checks if column exists in the table
    Parameters
    ----------
    column : Union[AnyStr, SQLite3xColumn]
        Name of column or SQLite3xColumn object.
    Returns
    ----------
    bool
        logical value of column's existence.
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

users = db['users'] # <--- HERE WE GOT SQLite3xTable

users.has_column('id')  # True
users.has_column('name')  # True
users.has_column('group')  # True
users.has_column('unknown_3301_C01UMN')  # False
```


### [Back to home](README.md)