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


debug_mode(True)

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

db.insert("groups", group_id=1, group_name="Admins")
db.insert("groups", group_id=2, group_name="Other")

db.insert('users', ['user_1', 1])
db.insert('users', ('user_2', 2))
db.insert('users', 'user_3', 2)
db.insert('users', username='user_4', group_id=1)
db.insert('users', username='user_5')
db.insert('users', {
    'username': 'user_6',
    'group_id': 1
})
db.insert(
    OR=REPLACE,
    TABLE='users',
    username='user_7', group_id=1
    )

db.insertmany(
    'about', group_id=[1, 2], description=['Damn cool goy', 'Just regular user']
)


# Have to fail

try:
    db.insert("users", group_id=1)
except IntegrityError:
    logger.info("INSERT #1 passed")
try:
    db.insert("groups", group_id=1, group_name="Fail")
except IntegrityError as e:
    logger.info("INSERT #2 passed")

####################################################
# SELECT data from DB
selects = []

selects.append(
    db.select(TABLE='users')
)

selects.append(
    db.select('users', ['username', 'group_id'])
)

selects.append(
    db.select(TABLE='users', SELECT=['username'])
)

selects.append(
    db.select(TABLE='users', WHERE={'group_id': 1})
)

selects.append(
    db.select(TABLE='users', WHERE={'group_id': 1, 'username': 'user_1'}, ORDER_BY='username')
)

selects.append(
    db.select(TABLE='users', WHERE={'group_id': 1}, ORDER_BY={'username': 'DESC'})
)

selects.append(
    db.select(TABLE='users', WHERE={'group_id': 1}, ORDER_BY=[2, 1])
)


selects.append(
    db.select(TABLE='users', WHERE={'group_id': 4}, execute=False)
)

selects.append(
    db.select(TABLE='users', SELECT='username', WHERE={'group_id': 1}, LIMIT=1)
)


logger.info(f"\nAll from users: {selects[0]}")
logger.info(f"\nUsernames and group_id from users: {selects[1]}")
logger.info(f"\nUsernames from users: {selects[2]}")
logger.info(f"\nAll from users where group_id=1: {selects[3]}")
logger.info(f"\nAll from users where group_id=1 and username=user_1, order_by username: {selects[4]}")
logger.info(f"\nAll from users where group_id=1, order_by username by DESC: {selects[5]}")
logger.info(f"\nAll from users where group_id=1, order_by [2,1]: {selects[6]}")
logger.info(f"\nScript SELECT where group_id=4: {selects[7].request.script}")
logger.info(f"\nOne record, one value: {selects[8]}")


####################################################
# SELECT data from DB
db.insertmany("users", [10, 1], [11, 2], [12, 3])
db.insertmany("users", [(20, 1), (21, 2), (23, 3)])
db.insertmany("users", [[30], [31, 2]])
db.insertmany("users", username=[41, 42, 43], group_id=[1, 2])

db.replace("groups", [1, 'AAdmins'])
db.replace("groups", group_id=2, group_name="IDK")

db.insert("users", username="user_411", group_id=1,
          OR=REPLACE,
          WITH={
              'a': db.select(
                  TABLE='users',
                  WHERE={'group_id': 1},
                  execute=False
              )}
          )

db.insert("users", ["user_422", 1],
          OR=REPLACE,
          WITH={
              'a': "SELECT * FROM users WHERE (group_id=2)"
          })

db.delete("users", WHERE={'username': 'user_422'})

db.update(TABLE="users", SET={'username': 'USER_upd', 'group_id': 2}, WHERE={'username': "user_411"})

# print(*db.tables)

db.drop("remove_me")

# print(*db.tables)

print(db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='about'")[0][0].split('\n'))

db.disconnect()

sleep(0.5)
rem = ''

while rem.lower() not in ['y', 'n']:
    rem = input(f"\n\nAll tests passed! \nRemove {DB_NAME}?: ")
    if rem == 'y':
        remove(f"{getcwd()}/{DB_NAME}")
