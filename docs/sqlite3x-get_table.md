# SQLite3x.get_tables

```python
def get_table(
        self,
        name: AnyStr
) -> SQLite3xTable:
    """
    Shadow method for __getitem__, that used as like: database['table_name']
    Get table object (SQLite3xTable instance)
    Parameters
    ----------
    name : AnyStr
        Name of table
    Returns
    ----------
    SQLite3xTable
        Instance of SQLite3xTable, table of database
    """
```

Same as `db['table_name']`


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

users_table = db.get_table('users')

print(type(users_table))   # SQLite3xTable

# OR ANOTHER WAY

users_table = db['users']

print(type(users_table))   # SQLite3xTable


users_table.insert([1, 'Alex'])

```

### [Back to home](./index.md)