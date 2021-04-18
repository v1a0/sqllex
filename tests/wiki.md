<div align="center">


# Welcome to the Sqllex Wiki! 👋



<br>
Here you can find some explanations and examples for Sqllex lib. <br>
</div><br>

## Chapters
- [About](#About)
- ### [Examples](#Examples)
- [SQLite3x Methods](#SQLite3x)

---

# About

### What the heck is Sqllex? 🤔

Sqllex is a python library created to make it easier for developers to interact with databases.
Currently, it supports only SQLite databases, but we’re planning to expand this list soon. 
SQLite is a nice and simple tool for administrating databases, but Sqllex makes it even more easy and comfortable.

It'll be a lot easier to show then explain.


# SQLite3x
## Examples
Imagine you need create some database, with structure like:


<table>
    <thead>
        <tr>
            <th colspan=3>Your awesome database</th>
        </tr>
        <tr>
            <th colspan=1>Table</th>
            <th colspan=1>Columns</th>
            <th colspan=1>Column params</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2><b>Groups</b></td>
            <td rowspan=1>id</td>
            <td><code>INTEGER PRIMARY KEY UNIQUE</code></td>
        </tr>
        <tr>
            <td>name</td>
            <td><code>TEXT NOT NULL DEFAULT 'Unknown'</code></td>
        </tr>
        <tr>
            <td rowspan=3><b>Users</b></td>
            <td>id</td>
            <td><code>INTEGER PRIMARY KEY UNIQUE</code></td>
        </tr>
        <tr>
            <td>username</td>
            <td><code>TEXT NOT NULL</code></td>
        </tr>
        <tr>
            <td>user_group</td>
            <td><code>FOREIGN KEY (user_group) REFERENCES groups (id)</code></td>
        </tr>
    </tbody>
</table>


[I don't need explains, just show me the code](#Code)


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

<details>
<summary id="just_code_1">Code without comments</summary>



```python

from sqllex import *


db = SQLite3x(path='my_awesome_db.db')

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

db.insert('groups', id=1, name="Admin")

db.insert('groups', [2, "User"])

db.insert('groups', 3, 'Guest')


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

db.insertmany('users', users_list)

users_in_db = db.select('username', 'users')

print(users_in_db)

users_group_1 = db.select(
    'username', 'users',
    WHERE={'user_group': 1}
)

print(users_group_1)
```
</details>


### Congratulation, now you know basic SQLite3x methods! Explore more features and method on the links down below.


## Public SQLite3x methods:

- insert
- insertmany
- update
- replace
- select
- - select_distinct
- - select_all
- markup
- create_table
- - create_temp_table
- - create_temporary_table
- delete
- drop
- get_columns
- pragma
- - foreign_keys
- - journal_mode
- - table_info
- execute
- executemany


