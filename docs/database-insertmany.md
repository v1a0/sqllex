# AbstractDatabase.insertmany

```python
def insertmany(
        self,
        TABLE: Union[AnyStr, AbstractTable],
        *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple, Iterable],
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
        Action in case if inserting has failed. Optional parameter.
        > OR='IGNORE'
    kwargs : Any
        An 2'st way set values for insert
    
    Returns
    ----------
        None or SQL-script in SQLStatement
    """
```


## Examples

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, TEXT, NOT_NULL, IGNORE

db: AbstractDatabase = ...


db.create_table(
    'users',
    {
        'id': [INTEGER],
        'name': [TEXT, NOT_NULL]
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

### [Back to home](README.md)
