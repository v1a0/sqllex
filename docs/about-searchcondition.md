# SearchCondition

Special class for generating condition with AbstractColumn.

## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER, sx.PRIMARY_KEY, sx.UNIQUE],
        'name': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, 'Unknown']
    }
)


id_col = db['users']['id']  # AbstractColumn
name_col = db['users']['name']  # AbstractColumn


db.update(
    TABLE='users',                            # table name
    SET=['username', 'Updated_name_0'],       # set username 'Updated_name_0'
    WHERE=(
            id_col == 1   # <---- SearchCondition !!!!
    )
)


db.update(
    'users',                            # table name
    ['username', 'Updated_name_1'],     # set username 'Updated_name_1'
    id_col > 1     # <---- SearchCondition !!!!
)


db.update(
    'users',
    SET={
        'name': 'Updated_name_1'
    },
    WHERE=(
        id_col == 1    # <---- SearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        name_col: name_col + '__UPDATED'     # <---- SearchCondition !!!!
    },
    WHERE=(
        id_col == 1    # <---- SearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        id_col: id_col + 420     # <---- SearchCondition !!!!
    },
    WHERE=(
        id_col == 1     # <---- SearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_id<2'
    },
    WHERE=(
        id_col < 2    # <---- SearchCondition !!!!
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_!=1_and_!=2'
    },
    WHERE=(
       (id_col != 1) & (id_col !=2)    # <---- SearchCondition !!!!
    ),
    OR=sx.IGNORE
)

db.update(
    'users',
    SET=['name', 'Updated_name_<4_or_=1'],
    WHERE=(
        (id_col < 4) | (id_col == 1)     # <---- SearchCondition !!!!
    )
)
```


### [Back to home](README.md)