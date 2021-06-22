# SQLite3x.update


```python
def update(
        self,
        TABLE: AnyStr,
        SET: Union[List, Tuple, Mapping],
        WHERE: WhereType = None,
        OR: OrOptionsType = None,
        WITH: WithType = None,
        **kwargs,
) -> None:
    """
    UPDATE, SET column_name=something WHERE x=y and more complex requests

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    SET : Union[List, Tuple, Mapping]
        Column and value to set
    WHERE : WhereType
        optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
    OR : OrOptionsType
        Optional parameter. If INSERT failed, type OrOptionsType
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


id_col = db['users']['id']  # !!!!
name_col = db['users']['name']  # !!!!


db.update(
    TABLE='users',                            # table name
    SET=['username', 'Updated_name_0'],       # set username 'Updated_name_0'
    WHERE=(
            id_col == 1                       # where id == 1
    )
)


db.update(
    'users',                            # table name
    ['username', 'Updated_name_1'],     # set username 'Updated_name_1'
    id_col > 1                          # where id > 1
)


db.update(
    'users',
    SET={
        'name': 'Updated_name_1'
    },
    WHERE=(
        id_col == 1
    )
)

db.update(
    'users',
    SET={
        name_col: name_col + '__UPDATED'    # SET id column name value == old value + '__UPDATED'
    },
    WHERE=(
        id_col == 1
    )
)

db.update(
    'users',
    SET={
        id_col: id_col + 420     # SET id column new value == old value + 420
    },
    WHERE=(
        id_col == 1
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_id<2'
    },
    WHERE=(
        id_col < 2
    )
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_!=1_and_!=2'
    },
    WHERE=(
       (id_col != 1) & (id_col !=2)
    ),
    OR=IGNORE
)

db.update(
    'users',
    SET=['name', 'Updated_name_<4_or_=1'],
    WHERE=(
        (id_col < 4) | (id_col == 1)
    )
)


# OLD variants
# for WHERE
#
# WHERE=['id', 4]
#
# WHERE={
#        'id': ['!=', [1,2]]
#       }
#
# WHERE={
#        'id': ['<', 2]
#      }
#
# WHERE="id>2"
#


```


### [Back to home](./index.md)