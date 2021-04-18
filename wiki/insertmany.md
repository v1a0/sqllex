<div align="center">

# SQLite3x.insertmany

</div><br>

## About

Method to INSERT many values into db's table.

```python
def insertmany(self,
               TABLE: AnyStr,
               *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
               execute: bool = True,
               **kwargs: Any
               ) -> Union[None, SQLStatement]:
```

>The same as regular insert but for lists of inserting values

>:param TABLE: Table name for inserting

>:param execute: Execute script and return db's answer (True) or return script (False)

>:param args: 1'st way set values for insert

>:param kwargs: 2'st way set values for insert


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

Read also:
- SQLite3x.insert