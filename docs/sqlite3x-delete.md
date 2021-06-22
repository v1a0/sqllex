# SQLite3x.delete


```python
def delete(
        self,
        TABLE: str,
        WHERE: WhereType = None,
        WITH: WithType = None,
        **kwargs,
) -> None:
    """
    DELETE FROM table WHERE {something}
    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    WHERE : WhereType
        optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
    WITH : WithType
        with_statement (don't really work well)
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


id_column = db['users']['id']


db.delete('users', id_column == 2)

db.delete(
    TABLE='users',
    WHERE=(
        id_column == 3
    )
)

db.delete(
    TABLE='users',
    WHERE=(
        id_column < 4
    )
)

db.delete(
    TABLE='users',
    WHERE=(
        (id_column != 5) & (id_column != 6) & (id_column != 7)
    )
)

```


### [Back to home](README.md)