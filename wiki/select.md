<div align="center">

# SQLite3x.select

</div><br>

## About

Method to SELECT data from table

```python
def select(self,
           SELECT: Union[List[str], str] = None,
           TABLE: str = None,
           FROM: str = None,
           WHERE: WhereType = None,
           WITH: WithType = None,
           ORDER_BY: OrderByType = None,
           LIMIT: LimitOffsetType = None,
           OFFSET: LimitOffsetType = None,
           execute: bool = True,
           **kwargs
           ) -> Union[SQLStatement, List[List]]:
```

> :param SELECT: columns to select. Value '*' by default

> :param TABLE: table for selection

> :param FROM: table for selection

> :param WHERE: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}

> :param WITH: with_statement

> :param ORDER_BY: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}

> :param LIMIT: optional parameter for conditions, example: 10

> :param OFFSET: optional parameter for conditions, example: 5

> :param :param execute: Execute script and return db's answer if True, return script if False

> :return: List[List] of selects


## Examples

```python

from sqllex import *

db = SQLite3x(path='database.db')

db.create_table(
    'users',
    {
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        'age': [INTEGER],
    }
)

...

db.select(ALL, 'users')

db.select(FROM='users')

db.select(ALL, 'users', ORDER_BY='age')

db.select(
    SELECT='name',
    TABLE='users',
    WHERE={
        'age': 10,    # where age = 10
    },
    ORDER_BY='age'
)

db.select(
    FROM='users',
    WHERE=['age', 10],    # where age = 10
    ORDER_BY=[1, 3]
)

db.select(
    TABLE='users',
    WHERE=['age', [10, 11]],    # where age = 10 and 11, wait a sec... i guess i fucked up...
    ORDER_BY='age'
)

db.select(
    FROM='users',
    WHERE=['age', '!=', 10],    # where age != 10
    ORDER_BY='age'
)

db.select(
    TABLE='users',
    WHERE={
        'age': 10,    # where age = 10
        'group': ['<', 10]    # and where group < 10
    },
    ORDER_BY='age'
)

db.select(
    FROM='users',
    WHERE={
        'age': 10,    # where age = 10
        'group': ['!=', 5, 10]    # where group != 5 and 10
    },
    ORDER_BY='age'
)


db.select(
    SELECT=['id', 'name'],
    FROM='users',
    WHERE={
        'age': ['>', 10],       # where age > 10
        'group': ['!=', 1]      # where group != 1
    },
    ORDER_BY=['age', 'ASC'],    # order by age ASC
    LIMIT=100,
    OFFSET=2
)


db.select(
    SELECT=ALL,
    TABLE='users',
    WHERE={
        'age': ['=', 10],       # where age = 10
        'group': ['<>', 1]      # where group <> 1
    },
    ORDER_BY='age DESC',        # order by age ASC
    LIMIT=50,
    OFFSET=20
)

```

Read also:
- SQLite3x.insert
- SQLite3x.update