# from sqllex import *
# columns = {
#         "username": [TEXT, NOT_NULL],
#         "group_id": INTEGER,
#
#         FOREIGN_KEY: {
#             "group_id": ["groups", "group_id"]
#         },
#     }
#
# temp = "TEMP"
# name = "groups"
# if_not_exist = True
#
# result: str = ''
#
# # column-def
# for (col, params) in columns.items():
#     if isinstance(params, (str, int, float)):
#         params = [f"{params}"]
#
#     if isinstance(params, list):
#         result += f"{col} {' '.join(param for param in params)},\n"
#
#     elif isinstance(params, dict) and col == FOREIGN_KEY:
#         res = ''
#         for (key, refs) in params.items():
#             res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
#         result += res[:-1]
#
#     else:
#         raise TypeError

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
    'groups',  # here is name of table
    {           # here is table structure
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],   # group id
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']    # group name
    }
)


"""
    And one more table
"""

db.create_table(
    name='users',  # here is name of table
    columns={
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],   # user id
        'username': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],    # user name
        'user_group': INTEGER,  # the group the user belongs to
        FOREIGN_KEY: {
            "user_group": ["groups", "id"]  # link to table groups, column id
        }
    })


"""
    Well done, now let's add some groups and some users indo your database
    For example:
        1: Admin 
        2: User
        3: Guest
"""

# Record some groups for the first

db.insert('groups', id=1, name="Admin") # You can add data like this

db.insert('groups', [2, "User"])    # Or like this

db.insert('groups', 3, 'Guest')    # Or like this


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
    (only usernames with group_id parameter equalised 1)
"""


users_group_1 = db.select(
    'username', 'users',
    WHERE={'user_group': 1}
)

print(users_group_1)


#if __name__ == '__main__':
#    pass

db.select(
    TABLE='users',
    WHERE={
        'group_id': 1,
        'username': 'user_1'
    },
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE={
        'group_id': 1,
        'username': 'user_1'
    },
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE=['age', 10],
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE=['age', [10, 11]],
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE=['age', '!=', 10],
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE=[
        ['age', '=', 10],
        ['age', 10]
    ],
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE={
        'age': 10,
        'group': ['<', 10]
    },
    ORDER_BY='username'
)

db.select(
    TABLE='users',
    WHERE={
        'age': 10,
        'group': [5, 10]
    },
    ORDER_BY='username'
)