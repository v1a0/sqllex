from sqllex import *
from os import walk, getcwd, remove
from typing import Any
from sqllex.types import SQLRequest
from sqllex.debug import debug_mode
from time import sleep


def is_exist(file: str = ''):
    return file in next(walk(getcwd()))[2]


class TestFailed(Exception):
    def __init__(self, why: str):
        self.why = why

    def __str__(self):
        return self.why


class Test:
    def __init__(self, n: int = 0):
        self.n = n

    def test(self, proc: Any, ret: list):
        if proc.request == SQLRequest(ret[0], ret[1]):
            logger.info(f'Test {self.n} passed')
            self.n += 1
        else:
            raise TestFailed(
                f"proc: {proc.request}\n"
                f"ret:  {SQLRequest(ret[0], ret[1])}"
            )


t = Test(n=1)

debug_mode(True)

DB_NAME = "test_database.db"

DB_TEMPLATE = {
    "groups": {
        "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
    },

    "users": {
        "username": [TEXT, NOT_NULL],
        "group_id": INTEGER,

        FOREIGN_KEY: {
            "group_id": ["groups", "group_id"]
        },
    },

    "remove_me": {
        "xxx": [INTEGER, PRIMARY_KEY, UNIQUE],
    },

}

####################################################
#          CREATE database by template
db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

if not is_exist(DB_NAME):
    raise TestFailed("DB is not exist")
else:
    logger.info("Creating database passed")

####################################################


####################################################
#                     INSERT


# 1
t.test(
    db.insert(
        TABLE="groups",
        group_id=1, name="Admins", execute=False
    ),

    [
        "INSERT INTO groups (group_id, name) VALUES (?, ?)",
        (1, 'Admins')
    ]
)

db.insert(
        TABLE="groups",
        group_id=1, name="Admins"
    )


# 2
t.test(
    db.insert(
        TABLE="groups",
        group_id=2, name="Other", execute=False
    ),

    [
        "INSERT INTO groups (group_id, name) VALUES (?, ?)",
        (2, 'Other')
    ]
)

db.insert(
        TABLE="groups",
        group_id=2, name="Other"
    )


# 3
t.test(
    db.insert('users', ['user_1', 1], execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_1', 1)]
)

db.insert('users', ['user_1', 1])


# 4
t.test(
    db.insert('users', ('user_2', 2), execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_2', 2)]
)

db.insert('users', ('user_2', 2))


# 5
t.test(
    db.insert('users', 'user_3', 2, execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_3', 2)]
)

db.insert('users', 'user_3', 2, execute=False)


# 6
t.test(
    db.insert('users', username='user_4', group_id=1, execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_4', 1)]
)

db.insert('users', 'user_3', 2)


# 7
t.test(
    db.insert('users', username='user_5', execute=False),
    ["INSERT INTO users (username) VALUES (?)", ('user_5',)]
)

db.insert('users', username='user_5')


# 8
t.test(
    db.insert('users', {'username': 'user_6', 'group_id': 1}, execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_6', 1)]
)

db.insert('users', {'username': 'user_6', 'group_id': 1})


# 9
t.test(
    db.insert('users', {'username': 'user_6', 'group_id': 1}, execute=False),
    ["INSERT INTO users (username, group_id) VALUES (?, ?)", ('user_6', 1)]
)


# 10
t.test(
    db.insert(
        OR=REPLACE,
        TABLE='users',
        username='user_7', group_id=1, execute=False
    ),
    ["INSERT OR REPLACE INTO users (username, group_id) VALUES (?, ?)", ('user_7', 1)]
)








# # N
# t.test(
#     db.insert(
#         OR=REPLACE,
#         TABLE='users',
#         username='user_7',
#         group_id='some',
#         WITH={
#             'some': db.select(
#                 SELECT='group_id',
#                 FROM='users',
#                 WHERE={'name': 'Admins'},
#                 execute=False)
#         },
#         execute=False
#     ),
#     ["WITH some AS (SELECT group_id FROM users WHERE (name=?)) INSERT OR REPLACE INTO users (username, group_id) "
#      "VALUES (?, some)", ('Admins', 'user_7')]
# )
#
# db.insert(
#         OR=REPLACE,
#         TABLE='users',
#         username='user_7',
#         group_id='some',
#         WITH={
#             'some': db.select(
#                 SELECT='group_id',
#                 FROM='users',
#                 WHERE={'name': 'Admins'},
#                 execute=False)
#         }
#     )







logger.success(f"\n\nAll tests passed!")
remove(f"{getcwd()}/{DB_NAME}")



# sleep(0.3)
# rem = ''
#
# while rem.lower() not in ['y', 'n']:
#     logger.success(f"\n\nAll tests passed! \nRemove {DB_NAME}?: ")
#     rem = input()
#     if rem == 'y':
#         remove(f"{getcwd()}/{DB_NAME}")





