<div align="center">

# SQLite3x.delete

</div><br>

## About

Method to DELETE FROM table WHERE __something__

```python
def delete(self,
           TABLE: str,
           WHERE: WhereType = None,
           WITH: WithType = None,
           execute: bool = True,
           **kwargs
           ) -> Union[None, SQLStatement]:
```



> :param TABLE: Table name as string

> :param WHERE: where_statement

> :param WITH: with_statement

>:param execute: Execute script and return db's answer (True) or return script (False)



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


db.delete('users',{'id': 2})

db.delete(
    TABLE='users',
    WHERE={'id': 3}
)

db.delete(
    TABLE='users',
    WHERE={'id': ['<', 4]}
)

db.delete(
    TABLE='users',
    WHERE={'id': ['!=', [5, 6, 7]]}
)

db.delete(
    TABLE='users',
    WHERE=['id', 5]
)

db.delete(
    TABLE='users',
    WHERE=['id', '>=', 6]
)

```

Read also:
- SQLite3x.insert