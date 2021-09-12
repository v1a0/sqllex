# AbstractTable

```python
class AbstractTable(ABC):
    """
    Sub-class of AbstractDatabase, itself one table inside ABDatabase
    Have same methods but without table name argument

    """

    def __init__(self, db, name: AnyStr):
        """
        Parameters
        ----------
        db : AbstractDatabase
            AbstractDatabase database object
        name : str
            Name of table
        """
```

## HOW TO USE

All methods of table-classes mostly similar to database-class. It's just don't have `TABLE` parameter.

It's so because object of this class already a TABLE, got it?

I guess you sharp person, but anyway I'll show you a few examples.


## Examples

```python
from sqllex.classes import AbstractDatabase, AbstractTable
from sqllex.constants.sqlite import *

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

# users: SQLite3xTable = db['users']

users.insert([1, 'Alex', 1])

users.insertmany(
    [
        [2, 'Blex', 2],
        [3, 'Clex', 1],
        [4, 'Dlex', 2],
    ]
)

users.select(ALL) # [(1, 'Alex', 1), (2, 'Blex', 2), (3, 'Clex', 1), (4, 'Dlex', 2)]

users.select(
    ALL,
    WHERE=(
        users['group'] == 1
    )
)  # [(1, 'Alex', 1), (3, 'Clex', 1)]


users.remove_column('group')

users.select(ALL) # [(1, 'Alex'), (2, 'Blex'), (3, 'Clex'), (4, 'Dlex')]

# And so on
```


### [Back to home](README.md)