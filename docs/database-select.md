# SQLite3x.select


```python
def select(
        self,
        SELECT: Union[
            AnyStr, AbstractColumn, ConstantType,
            List[Union[AbstractColumn, AnyStr]], Tuple[Union[AbstractColumn, AnyStr]]
        ] = None,
        WHERE: Union[WhereType, SearchCondition] = None,
        ORDER_BY: OrderByType = None,
        LIMIT: LimitOffsetType = None,
        OFFSET: LimitOffsetType = None,
        JOIN: JoinArgType = None,
        GROUP_BY: Union[GroupByType, AbstractColumn] = None,
        **kwargs,
) -> Tuple[Tuple]:
    """
    SELECT data from table

    Parameters
    ----------
    SELECT : Union[str, List[str]]
        columns to select. Value '*' by default
        > SELECT=['id', 'name']
    WHERE : WhereType
        optional parameter for conditions
        > db: AbstractDatabase
        > ...
        > WHERE=(db['table_name']['column_name'] == 'some_value')
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
    JOIN: Union[str, List[str], List[List[str]]]
        optional parameter for joining data from other tables ['groups'],
    GROUP_BY: Union[GroupByType, AbstractColumn]
         optional parameter for group data in database response

    Returns
    ----------
    Tuple[Tuple]
        Selected records

    """
```

## Parameters

| Parameter | Description |
| :---      | :---     |
| [TABLE](./all-parameters.md#table)     | Table name or table object SQLite3xTable to select from |
| [SELECT *](./all-parameters.md#select)    | Column or columns to select from table (ALL by default) |
| [WHERE *](./all-parameters.md#where)     | Expression that have to be true for selecting records |
| [ORDER_BY *](./all-parameters.md#order_by)  | Sort selected records in specific order |
| [LIMIT *](./all-parameters.md#limit)     | Limit selected values amount |
| [FROM *](./all-parameters.md#from)      | Same as TABLE, exists just for backward compatibility |
| [JOIN *](./all-parameters.md#join)      | JOIN data from another table |
| [GROUP_BY *](./all-parameters.md#group_by)  | Group elements by value from specific column or columns |

<small>* - optional parameter</small>

## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER],
        'name': [sx.TEXT, sx.NOT_NULL],
        'age': [sx.INTEGER],
    }
)

...

db.select('users', sx.ALL) # The same as: db.select(FROM='users')

db.select('users')      # without any args selecting ALL by default

db.select('users', sx.ALL, ORDER_BY='age')     # sorting by age column


age_column = db['users']['age']  # !!!
group_column = db['users']['group']  # !!!

db.select(
    TABLE='users',
    SELECT='name',
    WHERE=(
        age_column == 10    # where column users.age = 10
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
    SELECT=sx.ALL,
    WHERE=(
        (age_column == 10)
    ),
    ORDER_BY='age DESC',        # order by age ASC
    LIMIT=50,
    OFFSET=20
)
```


# JOIN EXAMPLES

## 1. Simples but not the best way

```python
import sqllex as sx

db = sx.SQLite3x(...)
some_table = db['some_table']
users = db['users']

# Old and simple way 
some_table.select(
    SELECT=[                                                                 # SELECT username, group_name, description
        'username',
        'group_name',
        'description'
    ],      
    JOIN=(                                                                   # JOIN
        ('groups', sx.AS, 'gr', sx.ON, 'users.group_id == gr.group_id'),           # INNER JOIN groups AS gr ON us.group_id == gr.group_id
        (sx.LEFT_JOIN, 'about', 'ab', sx.ON, 'ab.group_id == gr.group_id')         # LEFT JOIN about ab ON ab.group_id == gr.group_id
    ),
    WHERE= (users['username'] != 'user_1') & (users['username'] != 'user_2'),  # WHERE (users.username<>'user_1') AND (users.username<>'user_2')
    ORDER_BY='age DESC',                                                     # ORDER BY age DESC
    LIMIT=50,                                                                # LIMIT 50
    OFFSET=20                                                                # OFFSET 20
)
```

### SQL script

```shell
SELECT username, group_name, description
FROM x_table
INNER JOIN groups AS gr ON us.group_id == gr.group_id
LEFT JOIN about ab ON ab.group_id == gr.group_id
WHERE (users.username<>'user_1') AND (users.username<>'user_2')
ORDER BY age DESC
LIMIT 50
OFFSET 20
```


## 2. Better way

```python
# DATABASE SCHEMA
# {
#      'position': {
#          'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
#          'name': TEXT,
#          'description': [TEXT, DEFAULT, NULL],
#      },
#      'employee': {
#          'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
#          'firstName': TEXT,
#          'surname': TEXT,
#          'age': [INTEGER, NOT_NULL],
#          'positionID': INTEGER,
#
#          FOREIGN_KEY: {
#              'positionID': ['position', 'id']
#          }
#      },
#      'payments': {
#          'date': [TEXT],
#          'employeeID': INTEGER,
#          'amount': [INTEGER, NOT_NULL],
#          
#          FOREIGN_KEY: {
#              'positionID': ['employee', 'id']
#          },
#      }
# }

db['employee'].select(
    SELECT=[
        db['employee']['id'],
        db['employee']['firstName'],
        db['position']['name']
    ],
    JOIN=(
        sx.INNER_JOIN, db['position'],
        sx.ON, db['position']['id'] == db['employee']['positionID']
    ),
    ORDER_BY=(
        db['position']['id'],
        'DESC'
    )
)
```

### SQL script

```shell
SELECT e.id, e.firstName, p.name
FROM employee e 
INNER JOIN position p 
ON e.positionID == p.id 
ORDER BY e.positionID DESC
```

## 3. More than one JOIN

```python
# DATABASE SCHEMA
# {
#      'position': {
#          'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
#          'name': TEXT,
#          'description': [TEXT, DEFAULT, NULL],
#      },
#      'employee': {
#          'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
#          'firstName': TEXT,
#          'surname': TEXT,
#          'age': [INTEGER, NOT_NULL],
#          'positionID': INTEGER,
#
#          FOREIGN_KEY: {
#              'positionID': ['position', 'id']
#          }
#      },
#      'payments': {
#          'date': [TEXT],
#          'employeeID': INTEGER,
#          'amount': [INTEGER, NOT_NULL],
#          
#          FOREIGN_KEY: {
#              'positionID': ['employee', 'id']
#          },
#      }
# }

db['employee'].select(
    SELECT=[
        db['employee']['id'],
        db['employee']['firstName'],
        db['position']['name']
    ],
    JOIN=(
        (
            sx.LEFT_JOIN, db['position'],
            sx.ON, db['position']['id'] == db['employee']['positionID']
        ),
        (
            sx.INNER_JOIN, self.db['payments'],
            ON, db['employee']['id'] == db['payments']['employeeID']
        )
    ),
    ORDER_BY=(
        db['payments']['amount'],
        'DESC'
    )
)
```

### SQL script

```shell
SELECT e.id, e.firstName, p.name 
FROM employee e 
LEFT JOIN position p 
ON e.positionID == p.id 
INNER JOIN payments 
ON e.id == payments.employeeID 
ORDER BY payments.amount DESC
```

### [Back to home](README.md)