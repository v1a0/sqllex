# SQLite3x.select


```python
def select(
        self,
        TABLE: Union[str, List[str], SQLite3xTable] = None,
        SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
        WHERE: WhereType = None,
        WITH: WithType = None,
        ORDER_BY: OrderByType = None,
        LIMIT: LimitOffsetType = None,
        OFFSET: LimitOffsetType = None,
        FROM: Union[str, List[str], SQLite3xTable] = None,
        JOIN: Union[str, List[str], List[List[str]]] = None,
        _method="SELECT",
        **kwargs,
) -> Union[SQLStatement, List[Any]]:
    """
    SELECT data from table

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    SELECT : Union[str, List[str]]
        columns to select. Value '*' by default
    WHERE : WhereType
        optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
    WITH : WithType
        with_statement (don't really work well)
    ORDER_BY : OrderByType
        optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
    LIMIT: LimitOffsetType
        optional parameter for conditions, example: 10
    OFFSET : LimitOffsetType
        optional parameter for conditions, example: 5
    FROM : str
        Name of table, same at TABLE
    JOIN: Union[str, List[str], List[List[str]]]
        optional parameter for joining data from other tables ['groups'],
    _method: str
        DON'T CHANGE IT! special argument for unite select_all, select_distinct into select()

    Returns
    ----------
    List[List]
        selected data

    """
```

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

db.select('users', ALL) # The same as: db.select(FROM='users')

db.select('users')      # without any args selecting ALL by default

db.select('users', ALL, ORDER_BY='age')     # sorting by age column


age_column = db['users']['age']  # !!!
group_column = db['users']['group']  # !!!

db.select(
    TABLE='users',
    SELECT='name',
    WHERE=(
        age_column == 10,    # where column users.age = 10
    ),
    ORDER_BY='age'
)

db.select(
    'users',
    WHERE=(age_column == 10),    # where column users.age = 10
    ORDER_BY=[1, 3]
)

db.select(
    'users',
    WHERE=( age_column != 10 ),    # where age != 10
    ORDER_BY='age'
)

db.select(
    'users',
    WHERE=(
        (age_column == 10) & (group_column < 10)  # where age = 10 and where group < 10
    ),
    ORDER_BY='age'
)

db.select(
    'users',
    WHERE=(
        (age_column == 10) & (group_column != 5) & (group_column != 10)
    ),
    ORDER_BY='age'
)


db.select(
    FROM='users',
    SELECT=['id', 'name'],
    WHERE=(
        (age_column == 10)
    ),
    ORDER_BY=['age', 'ASC'],    # order by age ASC
    LIMIT=100,
    OFFSET=2
)


db.select(
    TABLE='users',
    SELECT=ALL,
    WHERE=(
        (age_column == 10)
    ),
    ORDER_BY='age DESC',        # order by age ASC
    LIMIT=50,
    OFFSET=20
)


# For some another table

x_table.select(
    SELECT=['username', 'group_name', 'description'],                        # SELECT username, group_name, description
    JOIN=[                                                                   # JOIN
        ['groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],              # INNER JOIN groups AS gr ON us.group_id == gr.group_id
        [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']        # CROSS JOIN about ab ON ab.group_id == gr.group_id
    ],
    WHERE= (x_table['username'] != 'user_1') & (x_table['username'] != 'user_2'),  # WHERE (users.username<>'user_1') AND (users.username<>'user_2')
    ORDER_BY='age DESC',                                                     # order by age DESC
    LIMIT=50,                                                                # limit = 50
    OFFSET=20                                                                # offset = 20
)

# Same as SQL script like
# SELECT username, group_name, description
# FROM x_table
# INNER JOIN groups AS gr ON us.group_id == gr.group_id
# CROSS JOIN about ab ON ab.group_id == gr.group_id
# WHERE (users.username<>'user_1') AND (users.username<>'user_2')
# ORDER BY age DESC
# LIMIT 50
# OFFSET 20
```


### [Back to home](README.md)