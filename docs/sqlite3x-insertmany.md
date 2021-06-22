<div align="center">

# SQLite3x.insertmany

</div><br>

## About

Method to INSERT many values into db's table. The same as regular insert but for lists of inserting values.

```python
def insertmany(
        self,
        TABLE: AnyStr,
        *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
        OR: OrOptionsType = None,
        **kwargs: Any,
) -> None:
    """
    INSERT many data into table.
    The same as regular insert but for lists of inserting values

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    args : Union[List, Tuple]
        1'st way set values for insert
        P.S: args also support numpy.array value
    OR : OrOptionsType
        Optional parameter. If INSERT failed, type OrOptionsType
    kwargs : Any
        An 2'st way set values for insert

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

users_list = [
    [0, "User_0"],
    [1, "User_1"],
    [2, "User_2"],
    [3, "User_3"],
    [4, "User_4"],
    [5, "User_5"],
    [6, "User_6"],
    [7, "User_7"],
    [8, "User_8"],
    [9, "User_9"],
]

db.insertmany('users', users_list)

db.insertmany(
    'users',
    users_list,
    OR=IGNORE, # REPLACE, FAIL, ABORT, ROLLBACK
)


users_list = [
    (0, "User_0"),
    (1, "User_1"),
    (2, "User_2"),
    (3, "User_3"),
    (4, "User_4"),
    (5, "User_5"),
    (6, "User_6"),
    (7, "User_7"),
    (8, "User_8"),
    (9, "User_9"),
]

db.insertmany('users', users_list)


users_list = [
    {'id': 0, 'name': "User_0"},
    {'id': 1, 'name': "User_1"},
    {'id': 2, 'name': "User_2"},
    {'id': 3, 'name': "User_3"},
    {'id': 4, 'name': "User_4"},
    {'id': 5, 'name': "User_5"},
    {'id': 6, 'name': "User_6"},
    {'id': 7, 'name': "User_7"},
    {'id': 8, 'name': "User_8"},
    {'id': 9, 'name': "User_9"},
]

db.insertmany('users', users_list)

```

### [Back to home](./index.md)
