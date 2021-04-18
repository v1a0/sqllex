<div align="center">

# SQLite3x.insert

</div><br>

## About

Method to INSERT data into db's table

```python
def insert(self,
               TABLE: AnyStr,
               *args: InsertData,
               OR: OrOptionsType = None,
               WITH: WithType = None,
               execute: bool = True,
               **kwargs: Any
               ) -> Union[None, SQLStatement]:
```

> :param TABLE: Table name for inserting

> :param *args: Insertable data as args

> :param OR: An optional parameter. If INSERT failed, type OrOptionsType

> :param WITH: Optional parameter.

> :param execute: Execute script and return db's answer (True) or return script (False)

> :param **kwargs: Insertable data as kwargs


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

db.insert('user', 1, 'User1')

db.insert('user', [2, "User2"])

db.insert('user', (3, 'User3'))

db.insert('user', id=4, name="User4")

db.insert(
    TABLE='user',
    id=5, name="User5"
)

db.insert('user', name="User6")

```

Read also:
- SQLite3x.insertmany