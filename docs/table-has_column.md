# AbstractTable.has_column

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
from sqllex.classes import AbstractDatabase, AbstractTable
from sqllex.constants import *

db: AbstractDatabase = ...

db.create_table(
    'users',
    {
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        'group': [INTEGER, NOT_NULL]
    }
)

users: AbstractTable = db['users'] # <--- HERE WE GOT AbstractTable

users.has_column('id')  # True
users.has_column('name')  # True
users.has_column('group')  # True
users.has_column('unknown_3301_C01UMN')  # False
```


### [Back to home](README.md)