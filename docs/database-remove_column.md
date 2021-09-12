# AbstractDatabase.remove_column

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
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, TEXT, NOT_NULL

db: AbstractDatabase = ...

db.create_table(
    'users',
    {
        'id': [INTEGER],
        'name': [TEXT, NOT_NULL],
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


### [Back to home](README.md)