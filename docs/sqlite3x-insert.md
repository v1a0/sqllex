<div align="center">

# SQLite3x.insert

</div><br>

## About

Method to INSERT data into db's table

```python
def insert(
        self,
        TABLE: AnyStr,
        *args: InsertData,
        OR: OrOptionsType = None,
        WITH: WithType = None,
        **kwargs: Any,
) -> None:
    """
    INSERT data into table

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    OR : OrOptionsType
        Optional parameter. If INSERT failed, type OrOptionsType
    WITH : WithType
        Optional parameter.

    Returns
    ----------
        None
    """
```

## Examples

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

db.insert('user', 1, 'User1')

db.insert('user', [2, "User2"])

db.insert('user', (3, 'User3'))

db.insert('user', id=4, name="User4")

db.insert(
    TABLE='user',
    id=5, name="User5"
)

db.insert('user', name="User6")

db.insert(
    'users',
    [100, 'Dex1'],
    OR=IGNORE  # REPLACE, FAIL, ABORT, ROLLBACK
)

db.insert(
    'users',
    [200, 'Dex2'],
    OR=REPLACE 
)

db.insert(
    'users',
    [300, 'Dex3'],
    OR=ABORT
)

```


### [Back to home](./index.md)