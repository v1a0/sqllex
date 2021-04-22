<div align="center">

# SQLite3x.select

</div><br>

## About

Method to SELECT data from table

```python
def select(self,
           TABLE: str = None,
           SELECT: Union[List[str], str] = None,
           WHERE: WhereType = None,
           WITH: WithType = None,
           ORDER_BY: OrderByType = None,
           LIMIT: LimitOffsetType = None,
           OFFSET: LimitOffsetType = None,
           execute: bool = True,
           FROM: str = None,
           JOIN: Union[str, List[str], List[List[str]]] = None,
           **kwargs
           ) -> Union[SQLStatement, List[List]]:
```


> :param TABLE: table for selection

> :param SELECT: columns to select. Value '*' by default

> :param WHERE: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}

> :param WITH: with_statement

> :param JOIN: optional parameter for joining data from other tables ['groups'],

> :param ORDER_BY: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}

> :param LIMIT: optional parameter for conditions, example: 10

> :param OFFSET: optional parameter for conditions, example: 5

> :param :param execute: Execute script and return db's answer if True, return script if False

> :param FROM: table for selection

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

db.select('users', ALL)

db.select(FROM='users')


db.select('users')

db.select('users', ALL, ORDER_BY='age')

db.select(
    TABLE='users',
    SELECT='name',
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
    FROM='users',
    SELECT=['id', 'name'],
    WHERE={
        'age': ['>', 10],       # where age > 10
        'group': ['!=', 1]      # where group != 1
    },
    ORDER_BY=['age', 'ASC'],    # order by age ASC
    LIMIT=100,
    OFFSET=2
)


db.select(
    TABLE='users',
    SELECT=ALL,
    WHERE={
        'age': ['=', 10],       # where age = 10
        'group': ['<>', 1]      # where group <> 1
    },
    ORDER_BY='age DESC',        # order by age ASC
    LIMIT=50,
    OFFSET=20
)


db.select(
        SELECT=['username', 'group_name', 'description'],
        FROM=['users', AS, 'us'],
        JOIN=[                                                            # JOIN data from other tables
            ['groups', AS, 'gr', ON, 'us.group_id == gr.group_id'],       # JOIN  
            [INNER_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']
        ],
        WHERE={'username': 'user_1'}
    )

# SELECT username, group_name, description 
# FROM users AS us 
# INNER JOIN groups AS gr ON us.group_id == gr.group_id 
# INNER JOIN about ab ON ab.group_id == gr.group_id 
# WHERE (username='user_1')


```

Read also:
- SQLite3x.insert
- SQLite3x.update