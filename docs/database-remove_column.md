# SQLite3x.remove_column

```python
def remove_column(  # !!!
        self,
        table: AnyStr,
        column: Union[AnyStr, AbstractColumn]
):
    """
    Removes column from the table
    
    Parameters
    ----------
    table : AnyStr
        Name of table
    column : Union[AnyStr, AbstractColumn]
        Name of column or AbstractColumn object.

    """
```

# Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER],
        'name': [sx.TEXT, sx.NOT_NULL],
        'group': [sx.INTEGER, sx.NOT_NULL]
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


### [Back to home](README.md)