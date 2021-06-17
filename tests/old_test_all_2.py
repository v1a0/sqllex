from sqllex import SQLite3x, INTEGER, PRIMARY_KEY, UNIQUE, TEXT, NOT_NULL, DEFAULT, FOREIGN_KEY, REPLACE, AUTOINCREMENT
from os import walk, getcwd, remove
from sqlite3 import IntegrityError
from loguru import logger
from time import sleep
from sqllex.debug import debug_mode


class TestFailed(Exception):
    def __init__(self, why: str):
        self.why = why

    def __str__(self):
        return self.why


def is_exist(file: str = ''):
    return file in next(walk(getcwd()))[2]


debug_mode(False)

DB_NAME = "test_table.db"

DB_TEMPLATE = {
    "groups": {
        "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "group_name": [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
    },

    "users": {
        "username": [TEXT, NOT_NULL],
        "group_id": INTEGER,

        FOREIGN_KEY: {
            "group_id": ["groups", "group_id"]
        },
    },

    "about": {
        "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "description": TEXT,

        FOREIGN_KEY: {
            "group_id": ["groups", "group_id"]
        },
    },

    "remove_me": {
        "tester1": [AUTOINCREMENT, INTEGER, PRIMARY_KEY],
        "xxx": [INTEGER, UNIQUE],
    },

}

####################################################
# CREATE database by template
db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

if not is_exist(DB_NAME):
    raise TestFailed("DB is not exist")
else:
    logger.info("Creating database passed")

# print(*db.tables)

####################################################
# INSERT data int DB and SELECT
# 1'st table

db.connect()

groups_table = db["groups"]
users_table = db["users"]
about_table = db["about"]

groups_table.insert(group_id=1, group_name="Admins")
groups_table.insert(group_id=2, group_name="Other")

users_table.insert(['user_1', 1])
users_table.insert(('user_2', 2))
users_table.insert('user_3', 2)
users_table.insert(username='user_4', group_id=1)
users_table.insert(username='user_5')
users_table.insert(
    {
        'username': 'user_6',
        'group_id': 1
    })
users_table.insert(
    OR=REPLACE,
    username='user_7', group_id=1
)


about_table.insertmany(
    group_id=[1, 2], description=['Damn cool goy', 'Just regular user']
)

# Have to fail

try:
    users_table.insert(group_id=1)
except IntegrityError:
    logger.info("INSERT #1 passed")
try:
    groups_table.insert(group_id=1, group_name="Fail")
except IntegrityError as e:
    logger.info("INSERT #2 passed")

####################################################
# SELECT data from DB
selects = []

selects.append(
    users_table.select_all()
)

selects.append(
    users_table.select(['username', 'group_id'])
)

selects.append(
    users_table.select(SELECT=['username'])
)

selects.append(
    users_table.select(WHERE={'group_id': 1})
)

selects.append(
    users_table.select(WHERE={'group_id': 1, 'username': 'user_1'}, ORDER_BY='username')
)

selects.append(
    users_table.select(WHERE={'group_id': 1}, ORDER_BY={'username': 'DESC'})
)

selects.append(
    users_table.select(WHERE={'group_id': 1}, ORDER_BY=[2, 1])
)

selects.append(
    users_table.select(WHERE={'group_id': 4})
)

logger.info(f"\nAll from users: {selects[0]}")
logger.info(f"\nUsernames and group_id from users: {selects[1]}")
logger.info(f"\nUsernames from users: {selects[2]}")
logger.info(f"\nAll from users where_ group_id=1: {selects[3]}")
logger.info(f"\nAll from users where_ group_id=1 and username=user_1, order_by username: {selects[4]}")
logger.info(f"\nAll from users where_ group_id=1, order_by username by DESC: {selects[5]}")
logger.info(f"\nAll from users where_ group_id=1, order_by [2,1]: {selects[6]}")
# logger.info(f"\nScript SELECT where_ group_id=4: {selects[7].request.script}")

####################################################
# SELECT data from DB
users_table.insertmany([10, 1], [11, 2], [12, 3])
users_table.insertmany([(20, 1), (21, 2), (23, 3)])
users_table.insertmany([[30], [31, 2]])
users_table.insertmany(username=[41, 42, 43], group_id=[1, 2])

groups_table.replace([1, 'AAdmins'])
groups_table.replace(group_id=2, group_name="IDK")

users_table.insert(
    username="user_411", group_id=1,
    OR=REPLACE,
    # WITH={
    #     'a': db.select(
    #         TABLE='users',
    #         WHERE={'group_id': 1},
    #         execute=False
    #     )}
)

users_table.insert(
    ["user_422", 1],
    OR=REPLACE,
    WITH={
        'a': "SELECT * FROM users WHERE (group_id=2)"
    })

users_table.delete(WHERE={'username': 'user_422'})

users_table.update(SET={'username': 'USER_upd', 'group_id': 2}, WHERE={'username': "user_411"})

# print(*db.tables)

remove_me_table = db['remove_me']
remove_me_table.drop()

# print(remove_me_table)
#
# print(*db.tables)

from sqllex import *

# DAAAAAAAAAAMMMNNNN COOOL
join_test = users_table.select(
    SELECT=['username', 'group_name', 'description'],
    JOIN=[
        [INNER_JOIN, 'groups', AS, 'gr', ON, 'users.group_id == gr.group_id'],
        ['about', 'ab', ON, 'ab.group_id == gr.group_id']
    ],
    # WHERE={'username': 'user_1'}
)

logger.info(join_test)

# print(db.execute("SELECT sql FROM sqlite_schema WHERE name = 'users';"))
# print(*db.tables)
sleep(0.2)
print(users_table.find(group_id=['!=', 2]))

db.disconnect()
sleep(0.5)
rem = ''

print("database removed")
remove(f"{getcwd()}/{DB_NAME}")
