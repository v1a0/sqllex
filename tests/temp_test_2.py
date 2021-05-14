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
# ['User_0', 'User_1', 'User_2', 'User_3', 'User_4', 'User_5', 'User_6', 'User_7', 'User_8', 'User_9']


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
# ['User_0', 'User_3', 'User_6', 'User_9']


# And for some another table (you have to create it before run this code)

users.select(
        SELECT=['username', 'group_name', 'description'],                 # SELECT username, group_name, description
        JOIN=[                                                            # JOIN
            ['groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],    ## INNER JOIN groups AS gr ON us.group_id == gr.group_id
            [CROSS_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id'] ## INNER JOIN about ab ON ab.group_id == gr.group_id
        ],
        WHERE={'username': 'user_1'},                                     # WHERE (username='user_1')
        ORDER_BY='age DESC',                                              # order by age ASC
        LIMIT=50,
        OFFSET=20                                                           
    )

# Same as SQL script like
# SELECT username, group_name, description
# FROM users
# INNER JOIN groups AS gr ON users.group_id == gr.group_id
# CROSS_JOIN about ab ON ab.group_id == gr.group_id
# WHERE (username='user_1')
# ORDER BY age DESC
# LIMIT 50
# OFFSET 20

db.disconnect() # unlock your database