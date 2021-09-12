# AbstractDatabase.select


```python
def select(
        self,
        TABLE: Union[AnyStr, AbstractTable] = None,
        SELECT: Union[AnyStr, AbstractColumn, List, Tuple] = None,
        WHERE: WhereType = None,
        WITH: WithType = None,
        ORDER_BY: OrderByType = None,
        LIMIT: LimitOffsetType = None,
        OFFSET: LimitOffsetType = None,
        FROM: Union[AnyStr, AbstractTable] = None,
        JOIN: JoinArgType = None,
        _method="SELECT",
        **kwargs,
) -> Tuple:
    """
    SELECT data from table
    
    Parameters
    ----------
    TABLE: Union[AnyStr, AbstractTable]
        Name of table
    SELECT : Union[str, List[str]]
        columns to select. Value '*' by default
        > SELECT=['id', 'name']
    WHERE : WhereType
       optional parameter for conditions
       > WHERE=(db['table_name']['column_name'] == 'some_value')
    WITH : WithType
        Disabled!
    ORDER_BY : OrderByType
        optional parameter for conditions
        > ORDER_BY=['age', 'DESC']
        > ORDER_BY='age DESC'
    LIMIT: LimitOffsetType
        Set limit or selecting records
        > LIMIT=10
    OFFSET : LimitOffsetType
        Set offset for selecting records
        > OFFSET=5
    FROM : str
        Name of table, same at TABLE
    JOIN: JoinArgType
        optional parameter for joining data from other tables ['groups'],
    _method: str
        DON'T CHANGE IT! special argument for unite select_all, select_distinct into select()
    
    Returns
    ----------
    List[Tuple]
        Tuple of Selected data
    """
```

## Examples

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, TEXT, NOT_NULL, ALL, AS, ON, CROSS_JOIN

db: AbstractDatabase = ...

db.create_table(
    'users',
    {
        'id': [INTEGER],
        'name': [TEXT, NOT_NULL],
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