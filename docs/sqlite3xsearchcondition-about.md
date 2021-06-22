# SQLite3xSearchCondition

Special class for generating condition with SQLite3xColumn.

## Examples

```python

from sqllex import *
from sqllex.classes import SQLite3xSearchCondition

db = SQLite3x(path='database.db')

db.create_table(
    'users',
    {
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
    }
)


id_col = db['users']['id']  # SQLite3xColumn
name_col = db['users']['name']  # SQLite3xColumn



db.update(
    TABLE='users',                            # table name
    SET=['username', 'Updated_name_0'],       # set username 'Updated_name_0'
    WHERE=(
            id_col == 1   # <---- SQLite3xSearchCondition !!!!
    )
)


db.update(
    'users',                            # table name
    ['username', 'Updated_name_1'],     # set username 'Updated_name_1'
    id_col > 1     # <---- SQLite3xSearchCondition !!!!
)


db.update(
    'users',
    SET={
        'name': 'Updated_name_1'
    },
    WHERE=(
        id_col == 1    # <---- SQLite3xSearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        name_col: name_col + '__UPDATED'     # <---- SQLite3xSearchCondition !!!!
    },
    WHERE=(
        id_col == 1    # <---- SQLite3xSearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        id_col: id_col + 420     # <---- SQLite3xSearchCondition !!!!
    },
    WHERE=(
        id_col == 1     # <---- SQLite3xSearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_id<2'
    },
    WHERE=(
        id_col < 2    # <---- SQLite3xSearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_!=1_and_!=2'
    },
    WHERE=(
       (id_col != 1) & (id_col !=2)    # <---- SQLite3xSearchCondition !!!!
    ),
    OR=IGNORE
)

db.update(
    'users',
    SET=['name', 'Updated_name_<4_or_=1'],
    WHERE=(
        (id_col < 4) | (id_col == 1)     # <---- SQLite3xSearchCondition !!!!
    )
)

```


### [Back to home](./index.md)