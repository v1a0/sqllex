# SQLite3x | Awesome example #1

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
            <td><code>FOREIGN KEY "user_group" REFERENCES groups "id"</code></td>
        </tr>
    </tbody>
</table>


[I don't need explains, just show me the code](#Code)


```python
# 
# For the first, you need to import all from Sqllex lib and init your database
# 

from sqllex import *

db = SQLite3x(path='my_awesome_db.db')  # Init-ing your database

db.connect()    # It'll lock yor database until you disconnect, but makes sqllex work damn faster


# 
# Ok, now we need to create your tables into a database,
# use create_table method (as SQL-like CREATE TABLE)
# 


                                                        # Creating Groups table
db.create_table(
    'groups',                                            # here is name of table
    {                                                    # here is table structure
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],            # group id
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']     # group name
    }
)


# 
# And one more table
# 

db.create_table(
    name='users',                                            # here is name of table
    columns={
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],                # user id
        'username': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],    # user name
        'user_group': INTEGER,                               # the group user belongs to
        FOREIGN_KEY: {
            "user_group": ["groups", "id"]                   # link to table groups, column id
        }
    })


# 
# Well done, now let's add some groups and some users into your database
# For example:
#     1: Admin
#     2: User
#     3: Guest
# 
# Record this data
#

groups = db['groups']   # Get table 'groups' from db as object

groups.insert(id=1, name="Admin") # You can insert data like this

groups.insert([2, "User"])        # Or like this

groups.insert(3, 'Guest')         # Or like this

#
# Same thing but without table object
# db.insert('groups', id=1, name="Admin")
# db.insert('groups', [2, "User"])
# db.insert('groups', 3, 'Guest')
#

# 
# Now let's add many users, like a large dataset
# 


# Down below is a list of users, format: [id, name, group_id]

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

users = db['users']     # Get table 'groups' from db as object

users.insertmany(users_list)    # Insert it all by one line

#
# Done!
# 
# Now we need to take it back by select method (as SQL-like SELECT)
# 

users_in_db = users.select('username')  # Without any special arguments == SELECT ALL (by default)

print(users_in_db)  # ['User_0', 'User_1', 'User_2', 'User_3', 'User_4', 'User_5', 'User_6', 'User_7', 'User_8', 'User_9']


# 
# Prefect, and now select some specific records
# For example: 
# only 'usernames' of records WHERE column 'user_group' == 1
# 


users_group_1 = users.select(
    'username',
    WHERE=(users['user_group'] ==  1),
)

# or you can set this argument different ways
#   WHERE={'user_group': 1}
#   WHERE=['user_group', 1]
#   WHERE="user_group = 1"


print(users_group_1)    # ['User_0', 'User_3', 'User_6', 'User_9']


#
# And some large example for some another imaginary table
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!! CODE DOWN BELOW WOULD NOT WORK !!!
# !!!  This is an example of syntax  !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
#

users.select(
    SELECT=['username', 'group_name', 'description'],                        # SELECT username, group_name, description
    JOIN=[                                                                   # JOIN
        ['groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],              # INNER JOIN groups AS gr ON us.group_id == gr.group_id
        [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']        # CROSS JOIN about ab ON ab.group_id == gr.group_id
    ],
    WHERE= (users['username'] != 'user_1') & (users['username'] != 'user_2'),  # WHERE (users.username<>'user_1') AND (users.username<>'user_2')
    ORDER_BY='age DESC',                                                     # order by age ASC
    LIMIT=50,                                                                # limit = 50
    OFFSET=20                                                                # offset = 20
)

# Same as SQL script like
# SELECT username, group_name, description
# FROM users
# INNER JOIN groups AS gr ON us.group_id == gr.group_id
# CROSS JOIN about ab ON ab.group_id == gr.group_id
# WHERE (users.username<>'user_1') AND (users.username<>'user_2')
# ORDER BY age DESC
# LIMIT 50
# OFFSET 20

db.disconnect() # unlock your database and save all changes
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
    WHERE=(users['user_group'] ==  1),
)

print(users_group_1)

users.select(
    SELECT=['username', 'group_name', 'description'],                        
    JOIN=[                                                                   
        ['groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],           
        [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id']        
    ],
    WHERE= (users['username'] != 'user_1') & (users['username'] != 'user_2'),
    ORDER_BY='age DESC',                                                     
    LIMIT=50,                                                                
    OFFSET=20                                                                
)

db.disconnect()
```
</details>


### Congratulation, now you know basic SQLite3x methods! Explore more features and method on the links down below.

### [Back to home](README.md)
