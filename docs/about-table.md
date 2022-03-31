# Table

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
import sqllex as sx

db = sx.SQLite3x(path='database.db')
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
# users: PostgreSQLxTable = db['users']

users.insert([1, 'Alex', 1])

users.insertmany(
    [
        [2, 'Blex', 2],
        [3, 'Clex', 1],
        [4, 'Dlex', 2],
    ]
)

users.select(sx.ALL) # [(1, 'Alex', 1), (2, 'Blex', 2), (3, 'Clex', 1), (4, 'Dlex', 2)]

users.select(
    sx.ALL,
    WHERE=(
        users['group'] == 1
    )
)  # [(1, 'Alex', 1), (3, 'Clex', 1)]


users.remove_column('group')

users.select(sx.ALL) # [(1, 'Alex'), (2, 'Blex'), (3, 'Clex'), (4, 'Dlex')]

# And so on
```


### [Back to home](README.md)