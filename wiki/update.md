<div align="center">

# SQLite3x.update

</div><br>

## About

Method to UPDATE record in table

```python
def update(self,
               TABLE: AnyStr,
               SET: Union[list, tuple, dict],
               WHERE: WhereType,
               OR: OrOptionsType = None,
               execute: bool = True,
               WITH: WithType = None, **kwargs):
```

> :param TABLE: Table name

> :param SET: Value to update

> :param WHERE: Where something

> :param OR: Optional parameter

> :param execute: Execute script and return db's answer if True, return script if False

> :param WITH: with_statement


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

...


db.update(
    'users',
    SET={
        'name': 'NEW_name_User1'
    },
    WHERE={
        'id': 1
    }
)

db.update(
    'users',
    SET={
        'name': 'NEW_name_User_<_2'
    },
    WHERE={
        'id': ['<', 2]
    }
)

db.update(
    'users',
    SET={
        'name': 'NEW_name_User_!=_1_and_2'
    },
    WHERE={
        'id': ['!=', [1,2]]
    },
    OR=IGNORE
)

db.update(
    'users',
    SET=['name', 'NEW_name_User4'],
    WHERE=['id', 4]
)

```

Read also:
- SQLite3x.insert
- SQLite3x.insertmany