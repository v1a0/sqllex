
<div align="center">

# SQLLEX alpha v0.1.6 📚

![Python:3.9](https://img.shields.io/badge/Python-3.9-green)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/V1A0/sqllex/alerts/)

<br>
Better than <b>sqlite3</b>. Seriously, try it out<br>
</div><br>

## Installation
```
pip install sqllex
```


## About
Use databases without thinking about SQL. Let me show you how sqllex makes
your life easier. Imagine you need create some database, save some data
into it and take it back. That's how your code will look like.

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
# Let's add record of  33 years old user named 'Sqllex'
# Dear db, please, into 'users' table values ['Sqllex', 33]
db.insert('users', ['Sqllex', 33])

# Dear db, please, select username(s) from table 'users' where column 'age' == 33
users = db.select('username', FROM='users', WHERE={'age': 33})

# Print it
print(users)  # ['Sqllex']
```


Ok, what if you need more complex structure with FOREIGN KEYs? Not a big deal.

```python
"""
    For the first, you need to import * (all) from Sqllex lib and init your database
"""


# import * (all) from Sqllex
from sqllex import *

# Init-ing your databse
db = SQLite3x(path='my_awesome_db.db')


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

db.insert('groups', id=1, name="Admin") # You can add data like this 

db.insert('groups', [2, "User"])        # Or like this

db.insert('groups', 3, 'Guest')         # Or like this


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

# Insert it by one line
db.insertmany('users', users_list)

# Done!


"""
    Now we need to take it back by select method (as SQL-like SELECT)
"""

# SELECT (what) FROM (where)
users_in_db = db.select('username', 'users')

print(users_in_db)
# It'll print:
# ['User_0', 'User_1', 'User_2', 'User_3', 'User_4', 'User_5', 'User_6', 'User_7', 'User_8', 'User_9']


"""
    Prefect, and now select some specific records 
    (only usernames where group_id parameter equalized 1)
"""


users_group_1 = db.select(
    'username', 'users',
    WHERE={'user_group': 1}
)

print(users_group_1)
# It'll print:
# ['User_0', 'User_3', 'User_6', 'User_9']
```

# [Not enough? Need examples? Read more in Sqllex Wiki! (link)](https://github.com/V1A0/sqllex/wiki)

-----
### Other
#### [TODO-list](todo.md)
