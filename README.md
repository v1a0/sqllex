
<div align="center">

# SQLLEX alpha v0.1.5 📚

![Python:3.9](https://img.shields.io/badge/Python-3.9-green)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/alerts/)

<br>
Better than <b>sqlite3</b>. Seriously, try it out<br>
</div><br>

## Installation
```
pip install sqllex
```


## About
Use databases without thinking about SQL. Let me show you how sqllex makes
your life easier. Imagine you need create some database, save some data
into it and take it back. That's how your code will look like.

```python
from sqllex import *

# Create some database, with simple structure
db = SQLite3x(
    path='my_data.db',
    template= {
        "users": {
            "username": [TEXT, NOT_NULL],
            "age": INTEGER,
        }
    }
)

# Insert some data
db.insert('users', ['Sqllex', 33])

# Take it back
users = db.select('username', from_table='users', where={'age': 33})

print(users)  # ['Squllex']
```


Ok, what if you need more complex structure with FOREIGN KEYs? Not a big deal.

```python
from sqllex import *

DB_TEMPLATE = {
    "groups": {
        "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
    },

    "users": {
        "username": [TEXT, NOT_NULL],
        "group_id": INTEGER,

        FOREIGN_KEY: {
            "group_id": ["groups", "group_id"]
        },
    }
}

# and do your business ...
```

What if I have LARGE dataset to insert? Still easy.

```python
...
# Your awesome dataset
dataset = [
    [3, "pi", 0],
    [1, "pi", 1],
    [4, "pi", 2],
    [1, "pi", 3],
    [5, "pi", 4],
    [9, "pi", 5],
    [2, "pi", 6],
    ...
]

# One line
db.insertmany('math', dataset)

# Done
```

# Advances

Ok ok, what if you are SUPER_PRO_1337_SQL_GOY, and you need 100% of SQL features. Check this out.

```python
from sqllex import *

db = SQLite3x(
    path='./path/my_awesome.db',
    template={
        "groups": {
            "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
            "name": [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        }
    }
)

# Insert some groups into groups table
db.insertmany(
    'groups',
    group_id=[1, 2],
    name=["Admin", "User"],
)


# Let's create a new table with some FOREIGN_KEYs
db.create_table(
    name='users',
    columns={
        "username": [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        "group_id": INTEGER,
        FOREIGN_KEY: {
            "group_id": ["groups", "group_id"]
        },
    },
    without_rowid=True,
    as_=__something__
)

# Insert some users into users table
db.insertmany(
    table='users',
    username=['User_1', 'User_2', 'User_3', 'User_4', 'User_5', 'User_6'],
    group_id=[1, 2, 1, 1, 2, 2]
)

db.insert(
    or_=REPLACE,
    table='users',
    username='User_4',
    group_id=1,
)

# ANd now take it back whith some conditions
users = db.select(
    select='username',
    table='users',
    where={
        'group_id': 2
    },
    order_by={
        'username': 'DESC'
    },
    with_=__something__,
    limit=10,
    offset=1,
    execute=True,
)

# and do your business ...
```

# [Not enough? Need examples? Read more in Sqllex Wiki! (link)](https://github.com/V1A0/sqllex/wiki)

-----
### Other
#### [TODO-list](todo.md)
