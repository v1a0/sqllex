# SQLite3xTable

```python
class SQLite3x:
    """
    Main SQLite3x Database Class

    Attributes
    ----------
    __connection : Union[sqlite3.Connection, None]
        SQLite connection
    __path : PathType
        Local __str__ to database (PathType)

    """

    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        Initialization

        Parameters
        ----------
        path : PathType
            Local __str__ to database (PathType)
        template : DBTemplateType
            template of database structure (DBTemplateType)

        """
```

## HOW TO USE

It's Main Parent class for all interaction with SQLite3 database. 

Have a few Child classes SQLite3xTable, SQLite3xColumn, SQLite3xSearchCondition.

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


# users: SQLite3xTable = db['users']

db.insert('users', [1, 'Alex', 1])

db.insertmany(
    'users',
    [
        [2, 'Blex', 2],
        [3, 'Clex', 1],
        [4, 'Dlex', 2],
    ]
)

db.select('users', ALL) # [[1, 'Alex', 1], [2, 'Blex', 2], [3, 'Clex', 1], [4, 'Dlex', 2]]

db.select(
    'users',
    ALL,
    WHERE=(
        db['users']['group'] == 1
    )
)  # [[1, 'Alex', 1], [3, 'Clex', 1]]


db.remove_column('users', 'group')

db.select('users', ALL) # [[1, 'Alex'], [2, 'Blex'], [3, 'Clex'], [4, 'Dlex']]

# And so on
```

### [Back to home](./index.md)