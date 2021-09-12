## How to use this document

Here you can find all possible parameter for sqllex databases methods.

```markdown
## TABLE <-- parameter

TABLE: Union[str, List[str], SQLite3xTable]  <-- expected data types

Table name or table object SQLite3xTable.  <-- description

<-- examples -->
TABLE = "my_table",  # string
...
<-- the end -->
```

### Usage
```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import TEXT, INTEGER

db: AbstractDatabase = ...

db.insert(
    "my_table", # <--- HERE !!! (TABLE is the fires parameter)
    (1, 'User'),
)

db.select(
    TABLE="my_table", # <--- HERE !!!
    SELECT=('name', 'age')
)
```

---

# All Parameters

## TABLE
```python
TABLE: Union[str, List[str], SQLite3xTable]
```

Table name or table object SQLite3xTable.

```python
TABLE = "my_table",  # string

TABLE = db['users'],  # SQLite3xTable

TABLE = ["my_awesome_table", "mat"],   # use alias "mat" in code instead of "my_awesome_table"
```

---

## SELECT
```python
SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]]
```

Parameter of select-like methods to specify selecting columns. Can be string or column object SQLite3xColumn,
or list of this types.

```python
from sqllex.constants import ALL

SELLCT = ALL,   # same as SELLCT = '*'

SELLCT = "id",  # select only id column

SELECT = ["id", "username"],  # List, select id and username columns

SELECT = ("id", "username"),  # Tuple, select id and username columns

SELECT = db['users']['id'],   # AbstractColumn, select only id column

SELECT = [db['users']['id'],  db['users']['username']],   # List[AbstractColumn], select id and username columns

SELECT = (db['users']['id'],  db['users']['username']),   # Tuple[AbstractColumn], select id and username columns

```

---

## WHERE
```python
WHERE: WhereType
```

parameter for highlighting the cells of the method action, in accordance with the specified pattern.

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import LIKE

db: AbstractDatabase = ...

# id == 1

WHERE="id=1",

WHERE=( db['users']['id'] == 1 ),

WHERE=['id', 1],

WHERE=('id', 1),

WHERE= {
    'id': 1
},

# id > 1

WHERE=( db['users']['id'] > 1 ),

WHERE=['id', '>', 1],

WHERE= {
    'id': ['>', 1]
},

# id > 1 AND id < 5

WHERE=(
    (db['users']['id'] > 1) & (db['users']['id'] < 5)
),

# id == 1 OR id == 5

WHERE=(
    (db['users']['id'] == 1) | (db['users']['id'] == 5)
),

# users.name contains "foo"

WHERE=(
    (db['users']['name'] |LIKE| "%foo%"
),
```

---

## SET
```python
SET: Union[List, Tuple, Mapping]
```

Parameter of update-like methods, setting new value for selected records

```python
SET=[1, 'Alex'],

SET=(1, "Alex"),

SET = {
    'id': 1,
    'name': "Alex"
},

SET = {
    db['users']['id']: 1,
    db['users']['name']: "Alex"
},
```

---

## OR
```python
OR: OrOptionsType
```

Parameter sets what should database do in exception (fail) case


```python
from sqllex.constants import IGNORE, REPLACE, ABORT, FAIL, ROLLBACK

OR = IGNORE,

OR = REPLACE,

OR = ABORT,

OR = FAIL,

OR = ROLLBACK,

OR = 'IGNORE',
```

---

## ~~WITH~~
```python
WITH: WithType
```

Temporary disabled

---

## ORDER_BY
```python
ORDER_BY: Union[str, int, AbstractColumn, List[int, str, AbstractColumn], List[List[int, str, AbstractColumn]]]
```

An optional parameter to set ordering of selected elements. Awaiting column or lost of columns with ordering parameter

```python
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

ORDERD_BY = "id",

ORDERD_BY = "ASC",

ORDERD_BY = "DESC",

ORDERD_BY = "id ASC",

ORDERD_BY = "id DESC",

ORDERD_BY = ["id", "name"],

ORDERD_BY = ["id ASC", "name"],

ORDERD_BY = [["id", "ASC"], ["name", "DESC"]],

ORDERD_BY = db['users']['id'],

ORDERD_BY = [db['users']['id'], "ASC"],

# Coming soon 
# ORDERD_BY = [["id", ASC], ["name", DESC]],
# ORDERD_BY = ASC,
```

---

## LIMIT
```python
LIMIT: Union[int, str]
```

Parameter setting limit of how many columns select from a table.

```python
LIMIT = 42,

LIMIT = '42',
```

---

## OFFSET
```python
OFFSET: Union[int, str]
```

Parameter to set how many first records skip from the first one.

```python
OFFSET = 42,

OFFSET = '42',
```

---

## ~~FROM~~
```python
FROM: Union[str, List[str], AbstractTable]
```

Shadow name for [TABLE parameter](#table)

---

## JOIN
```python
JOIN: Union[str, List[str], List[List[str]]]
```

SQL JOIN-ing.

```python
from sqllex.classes import AbstractDatabase, AbstractTable
from sqllex.constants import AS, ON, CROSS_JOIN, INNER_JOIN

db: AbstractDatabase = ...
users: AbstractTable = db['users']

db.select(
    TABLE='users',
    SELECT=['username', 'group_name', 'description'],                        
    JOIN=[                                                                   
        ['groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],            # INNER JOIN by default     
        [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']        
    ],
    WHERE= (users['username'] != 'user_1') & (users['username'] != 'user_2')                                                               
)


JOIN=[                                                                   
        [INNER_JOIN, 'groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],         
        [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']        
    ],

JOIN=[                                                                   
        ['groups', 'gr', ON, 'users.group_id == gr.group_id'],       # INNER JOIN by default    
        ['about', 'ab', ON, 'ab.group_id == gr.group_id']           # INNER JOIN by default    
    ],

JOIN=[                                                                   
        ['groups', ON, 'users.group_id == groups.group_id'],       # INNER JOIN by default    
        ['about', ON, 'about.group_id == groups.group_id']           # INNER JOIN by default    
    ],

JOIN=[                                                                   
        ['groups', ON, 'users.group_id == groups.group_id'],       # INNER JOIN by default    
    ],
```

---

### [Back to home](README.md)