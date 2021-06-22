# SQLite3xTable

```python
class SQLite3xTable:
    """
    Sub-class of SQLite3x contains one table of Database
    Have same methods but without table name argument

    Attributes
    ----------
    db : SQLite3x
        SQLite3x database object
    name : str
        Name of table

    columns = list
        Generator of columns in table

    columns_names = list
        Generator of column's names in table

    """

    def __init__(self, db, name: AnyStr):
        """
        Parameters
        ----------
        db : SQLite3x
            SQLite3x database object
        name : str
            Name of table

        """
```

## HOW TO USE

All methods of this class mostly similar to class's SQLite3x. It's just don't have `TABLE` parameter/argument.

It's so because object of this class already a TABLE, got it?

I guess you sharp person, but anyway I'll show you a few examples.

## Examples

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

# users: SQLite3xTable = db['users']

users.insert([1, 'Alex', 1])

users.insertmany(
    [
        [2, 'Blex', 2],
        [3, 'Clex', 1],
        [4, 'Dlex', 2],
    ]
)

users.select(ALL) # [[1, 'Alex', 1], [2, 'Blex', 2], [3, 'Clex', 1], [4, 'Dlex', 2]]

users.select(
    ALL,
    WHERE=(
        users['group'] == 1
    )
)  # [[1, 'Alex', 1], [3, 'Clex', 1]]


users.remove_column('group')

users.select(ALL) # [[1, 'Alex'], [2, 'Blex'], [3, 'Clex'], [4, 'Dlex']]

# And so on
```


### [Back to home](./index.md)