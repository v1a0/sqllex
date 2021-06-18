# Sqllex v0.1.10.0

## SELECT structure changed !!!

Now you have to combine selecting columns into `list` or `tuple`:

#### RIGHT!

```python
db.select('users', ['id', 'name'], ... ) 
```

#### WRONG!

```python
db.select('users', 'id', 'name', ... ) 
```

Error:
```shell
Traceback (most recent call last):
  File "C:\Users\User\GitHub\sqllex\tests\new_test_all.py", line 1, in select_test
    db.select('users', 'id', 'name', ... )
TypeError: select() got multiple values for argument 'WHERE'
```

### WHY?

In update 0.1.10.0 expecting arguments for select method changed

#### Old structure: 

```python
def select(
        self,
        TABLE: Union[str, List[str]] = None,
        *args: Union[str, List[str]], # <----- this line!!!
        SELECT: Union[str, List[str]] = None,
        WHERE: WhereType = None,
        ...
        **kwargs,
) -> Union[SQLStatement, List[Any]]:
```

#### New structure: 

As you see `**args` handling removed

```python
def select(
        self,
        TABLE: Union[str, List[str], SQLite3xTable] = None,
        SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
        WHERE: WhereType = None,
        ...
        _method="SELECT",
        **kwargs,
) -> Union[SQLStatement, List[Any]]: ...
```

## WHERE

Now you can set `WHERE` condition like this: 
```python
users = db['users']

users.select(
    SELECT=users['name'],
    WHERE=( users['id'] == 2 )
)

# OR (the same)

users.select(
    'name',
    users['id'] == 2
)

```

### EXAMPLE

```python
from sqllex import SQLite3x, INTEGER, TEXT, ALL

db = SQLite3x(path='test.db')

db.create_table(
    'users',
    {
        'id': INTEGER,
        'name': TEXT
    }
)

# Get table from database as object
users = db['users']

# Get column from table as object
urs_id = users['id']

# Get another column from table as object
usr_name = users['name']

print(users.columns_names)  # ['id', 'name']


# Inserting data
users.insert([1, 'Alex'])
users.insert([2, 'Blex'])


# SELECT * FROM users WHERE (users.id=2) OR (users.id=1)
users.select(ALL, (urs_id == 2) | (urs_id == 1))    # [[1, 'Alex'], [2, 'Blex']]


# Update name WHERE (id=1)
users.update(
    {'name': "XXXX"},
    WHERE=urs_id == 1
)


# SELECT * FROM users WHERE (users.id<>0) AND (users.id<>1)
users.select(
    [usr_name, urs_id],
    WHERE=(
        (urs_id != 0) & (urs_id != 1)
    )
)   # [['XXXX', 1], ['Blex', 2]]


# UPDATE id SET id = id + 2 WHERE (name = "XXXX")
users.update(
        {
            urs_id: urs_id + 2
        },
        WHERE=usr_name == 'XXXX'
)


users.select([usr_name, urs_id], WHERE=(urs_id == 3))   # [['XXXX', 3]]
```

---