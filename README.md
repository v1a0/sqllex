
<div align="center">

<img src="./pics/sqllex-logo.svg" width="300px">

# SQLLEX alpha v0.1.9 📚

![Python:3.9](https://img.shields.io/badge/Python-3.9-green)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/alerts/)
    
    
<br>
Better than <b>sqlite3</b>. Seriously, try it out<br>
</div><br>

## Installation
```shell
pip install sqllex
```

If you need most stable version install **sqllex==0.1.9.4**

| Version |  Status | Tests, and actions |
| :--------: | :----------------------------: | :---: |
| `0.1.9.10`     | ⚠️ unstable <br> ✔️ supported      | [![CodeQL](https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml) </br> [![Test Sqlite3x](https://github.com/v1a0/sqllex/actions/workflows/test_sqlite3x.yml/badge.svg?branch=main)](https://github.com/v1a0/sqllex/actions/workflows/test_sqlite3x.yml) </br> [![Upload Python Package](https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml/badge.svg)](https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml) |
| `0.1.9.4`     | ✔️ stable   <br> ✔️ supported      |  ✔️All passed |
| `<= 0.1.8.12` | ✔️ stable   <br> ❌️ outdated       |  ~ |



## About
Use databases without thinking about SQL. Let me show you how sqllex makes
your life easier. Imagine you need create some database, save some data
into it and take it back. That's how your code will look like.

### If you never used SQLite before read [this awesome example](https://github.com/v1a0/sqllex/wiki/SQLite3x-%7C-SIMPLEST-EXAMPLE#simplest-sqlite3x-example) or [this one](https://deepnote.com/@abid/SQLLEX-Simple-and-Faster-7WXrco0hRXaqvAiXo8QJBQ#)
```python
from sqllex import *

db = SQLite3x(                              
    path='my_database.db',                      
    template={                              
        "users": {                          
            "username": [TEXT, NOT_NULL],   
            "age": INTEGER,                 
        }                                   
    }                                       
)

users = db["users"]

users.insert('Sqllex', 33)

user = users.find(age=33)

print(users)  # [['Sqllex', 33]]
```

<br>
<details>
<summary id="what1"><big>WHAT IS GOING ON THERE?!</big></summary>

```python
from sqllex import *

# Create some database, with simple structure
db = SQLite3x(                              # create database 
    path='my_data.db',                      # path to your database, or where you would like it locate
    template={                              # schema for tables inside your database                              
        "users": {                          # name for the 1'st table
            "username": [TEXT, NOT_NULL],   # 1'st column of table, named "username", contains text-data, can't be NULL
            "age": INTEGER,                 # 2'nd column of table, named "age", contains integer value
        }                                   # end of table
    }                                       # end of schema (template)
)

# Ok, now you have database with table inside it.
# Let's take this table as variable
users = db["users"]

# Now add record of 33 years old user named 'Sqllex' into it
# Dear table, please insert ['Sqllex', 33] values 
users.insert('Sqllex', 33)

# Dear table, please find records where column 'age' == 33
user = users.find(age=33)

# Print results
print(users)  # [['Sqllex', 33]]
```

</details>

Ok, what if you need more complex structure with FOREIGN KEYs? Not a big deal.

```python
"""
    For the first, you need to import * (all) from Sqllex lib and init your database
"""


# import * (all) from Sqllex
from sqllex import *

# Init-ing your databse
db = SQLite3x(path='my_awesome_db.db')

db.connect()    # It'll lock yor database until you disconnect, but makes sqllex work damn faster

"""
    Ok, now we need to create your tables into a database,
    use create_table method (as SQL-like CREATE TABLE)
"""


# Creating Groups table
db.create_table(
    'groups',                                            # here is name of table
    {                                                    # here is table structure
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],            # group id
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']     # group name
    }
)


"""
    And one more table
"""

db.create_table(
    name='users',  # here is name of table
    columns={
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],                # user id
        'username': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],    # user name
        'user_group': INTEGER,                               # the group user belongs to
        FOREIGN_KEY: {
            "user_group": ["groups", "id"]                   # link to table groups, column id
        }
    })


"""
    Well done, now let's add some groups and some users into your database
    For example:
        1: Admin
        2: User
        3: Guest
"""

# Record some groups for the first

groups = db['groups']

groups.insert(id=1, name="Admin") # You can add data like this

groups.insert([2, "User"])        # Or like this

groups.insert(3, 'Guest')         # Or like this


# Same but without table object
# db.insert('groups', id=1, name="Admin")
# db.insert('groups', [2, "User"])
# db.insert('groups', 3, 'Guest')

"""
    Now let's add many users
"""


# Here we have a list of users in format: [id, name, group_id]
users_list = [
    [0, "User_0", 1],
    [1, "User_1", 2],
    [2, "User_2", 3],
    [3, "User_3", 1],
    [4, "User_4", 2],
    [5, "User_5", 3],
    [6, "User_6", 1],
    [7, "User_7", 2],
    [8, "User_8", 3],
    [9, "User_9", 1],
]

users = db['users']

# Insert it by one line
users.insertmany(users_list)

# Done!


"""
    Now we need to take it back by select method (as SQL-like SELECT)
"""

# SELECT FROM (table) (what)
users_in_db = users.select('username')

print(users_in_db)
# It'll print:
# [['User_0',] ['User_1'], ['User_2'], ['User_3'], ['User_4'], ['User_5'], ['User_6'], ['User_7'], ['User_8'], ['User_9']]


"""
    Prefect, and now select some specific records
    (only usernames where group_id parameter equalized 1)
"""


users_group_1 = users.select(
    'username',
    WHERE={'user_group': 1}
)

print(users_group_1)
# It'll print:
# [['User_0'], ['User_3'], ['User_6'], ['User_9']]


# And for some another table

users.select(
        SELECT=['username', 'group_name', 'description'],                 # SELECT username, group_name, description
        WITH=['users', AS, 'us'],                                         # FROM users AS us
        JOIN=[                                                            # JOIN
            ['groups', AS, 'gr', ON, 'us.group_id == gr.group_id'],       ## INNER JOIN groups AS gr ON us.group_id == gr.group_id
            [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id'] ## INNER JOIN about ab ON ab.group_id == gr.group_id
        ],
        WHERE={'username': 'user_1'},                                     # WHERE (username='user_1')
        ORDER_BY='age DESC',                                              # order by age ASC
        LIMIT=50,
        OFFSET=20                                                           
    )

# Same as SQL script like
# SELECT username, group_name, description
# FROM users AS us
# INNER JOIN groups AS gr ON us.group_id == gr.group_id
# CROSS_JOIN about ab ON ab.group_id == gr.group_id
# WHERE (username='user_1')
# ORDER BY age DESC
# LIMIT 50
# OFFSET 20

db.disconnect() # unlock your database

```


<details>
<summary id="just_code_1">Code without comments</summary>



```python

from sqllex import *

db = SQLite3x(path='my_awesome_db.db')

db.connect()


db.create_table(
    'groups',                                            
    {                  
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
    }
)

db.create_table(
    name='users',
    columns={
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'username': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        'user_group': INTEGER,
        FOREIGN_KEY: {
            "user_group": ["groups", "id"]
        }
    })

groups = db['groups']

groups.insert(id=1, name="Admin")

groups.insert([2, "User"])

groups.insert(3, 'Guest')

users_list = [
    [0, "User_0", 1],
    [1, "User_1", 2],
    [2, "User_2", 3],
    [3, "User_3", 1],
    [4, "User_4", 2],
    [5, "User_5", 3],
    [6, "User_6", 1],
    [7, "User_7", 2],
    [8, "User_8", 3],
    [9, "User_9", 1],
]

users = db['users']

users.insertmany(users_list)

users_in_db = users.select('username')

print(users_in_db)

users_group_1 = users.select(
    'username',
    WHERE={'user_group': 1}
)

print(users_group_1)

users.select(
        SELECT=['username', 'group_name', 'description'], 
        WITH=['users', AS, 'us'],
        JOIN=[                                   
            ['groups', AS, 'gr', ON, 'us.group_id == gr.group_id'],
            [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']
        ],
        WHERE={'username': 'user_1'},                                     
        ORDER_BY='age DESC',                                             
        LIMIT=50,
        OFFSET=20                                                           
    )

db.disconnect()

```
</details>

# [Not enough? Need examples? Read more in Sqllex Wiki! (link)](https://github.com/V1A0/sqllex/wiki)

-----
### Other
#### [TODO-list](todo.md)
