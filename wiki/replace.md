<div align="center">

# SQLite3x.replace

</div><br>

## About

Method to REPLACE data into db's table

```python
def replace(self,
            TABLE: AnyStr,
            *args: Any,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs: Any
            ) -> Union[None, SQLStatement]:
```

> :param TABLE: Table name for inserting

> :param *args: Replaceable data as args

> :param WITH: Optional parameter.

> :param execute: Execute script and return db's answer (True) or return script (False)

> :param **kwargs: Replaceable data as kwargs


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

db.replace('user', 1, 'User1')

db.replace('user', [2, "User2"])

db.replace('user', (3, 'User3'))

db.replace('user', id=4, name="User4")

db.replace(
    TABLE='user',
    id=5, name="User5"
)



```

Read also:
- SQLite3x.insert