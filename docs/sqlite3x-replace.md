# SQLite3x.replace

```python
def replace(
        self,
        TABLE: AnyStr,
        *args: Any,
        WITH: WithType = None,
        **kwargs: Any,
) -> None:
    """
    REPLACE data into table, works only for records contains UNIQUE column

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    WITH : WithType
        Optional parameter.

    Returns
    ----------
        None or SQL-script in SQLStatement

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

...

db.replace('users', 1, 'User1')

db.replace('users', [2, "User2"])

db.replace('users', (3, 'User3'))

db.replace('users', id=4, name="User4")

db.replace(
    TABLE='users',
    id=5, name="User5"
)

# for SQLIte3xTable

users = db['users']

users.replace([5, "User5"])

```


### [Back to home](./index.md)