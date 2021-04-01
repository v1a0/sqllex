
<div align="center">

# SQLLEX alpha v0.1.2 📚

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
Use databases without thinking about SQL. Let's see how sqllex makes
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

print(users)  # [('Squllex',)]
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

### [TODO-list](todo.md)

### Not enough? Read more about methods and features in docs!
