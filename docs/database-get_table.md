# SQLite3x.get_tables

```python
def get_table(
        self,
        name: AnyStr
) -> AbstractTable:
    """
    Shadow method for __getitem__, that used as like: database['table_name']
    Get table object (AbstractTable instance)
    
    Parameters
    ----------
    name : AnyStr
        Name of table
        
    Returns
    ----------
    AbstractTable
        Instance of AbstractTable, table of database
    """
```

Same as `db['table_name']`


```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER],
        'name': [sx.TEXT, sx.NOT_NULL]
    }
)

users_table = db.get_table('users')

print(type(users_table))   # SQLite3xTable

# OR ANOTHER WAY

users_table = db['users']

print(type(users_table))   # SQLite3xTable


users_table.insert([1, 'Alex'])

```

### [Back to home](README.md)