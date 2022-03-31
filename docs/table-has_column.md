# SQLite3x.has_column

```python
def has_column(self, column: Union[AnyStr, AbstractTable]) -> bool:
    """
    Checks if column exists in the table
    
    Parameters
    ----------
    column : Union[AnyStr, AbstractColumn]
        Name of column or AbstractColumn object.
    
    Returns
    ----------
    bool
        logical value of column's existence.
    """
```

# Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='db-1.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER, sx.PRIMARY_KEY, sx.UNIQUE],
        'name': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, 'Unknown'],
        'group': [sx.INTEGER, sx.NOT_NULL]
    }
)

users: sx.SQLite3xTable = db['users'] # <--- HERE WE GOT AbstractTable

users.has_column('id')  # True
users.has_column('name')  # True
users.has_column('group')  # True
users.has_column('unknown_3301_C01UMN')  # False
```


### [Back to home](README.md)