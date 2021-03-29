from sqllex import SQLite3x, INTEGER, PRIMARY_KEY, UNIQUE, TEXT, NOT_NULL, DEFAULT, FOREIGN_KEY, ExecuteError, WITH
from os import walk, getcwd, remove
from loguru import logger


class TestFailed(Exception):
    def __init__(self, why: str):
        self.why = why

    def __str__(self):
        return self.why


def is_exist(file: str = ''):
    return file in next(walk(getcwd()))[2]


DB_NAME = "test_table.db"

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
    }
}


####################################################
# CREATE database by template
db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

db.insert('users', ["user_1", 1],
          WITH={
              'some': db.select('*', 'users', execute=False)
          }
          )

if not is_exist(DB_NAME):
    raise TestFailed("DB is not exist")
else:
    logger.info("Creating database passed")


####################################################
# INSERT data int DB and SELECT
# 1'st table
db.insert("groups", group_id=1, name="Admins")
db.insert("groups", group_id=2, name="Other")
# Have to fail
try:
    db.insert("groups", group_id=2, name="Other")
except ExecuteError:
    logger.info("INSERT #1 passed")


####################################################
# 2'nd table
db.insert("users", ["user_1", 1])
db.insert("users", ("user_2", 2))
db.insert("users", "user_3", 2)
db.insert("users", username="user_4", group_id=1)
db.insert("users", username="user_5")
db.insert("users", {
    'username': "user_6",
    'group_id': 1
})


# Have to fail
try:
    db.insert("users", group_id=1)
except ExecuteError:
    logger.info("INSERT #2 passed")


####################################################
# SELECT data from DB
logger.info(
    f"All from users: "
    f"{db.select(from_table='users')}\n"
)

logger.info(
    f"All from users: "
    f"{db.select(['username', 'group_id'], 'users')}"
)

logger.info(
    f"Usernames from users: "
    f"{db.select(select=['username'], from_table='users')}"
)

logger.info(
    f"All from users where group_id=1: "
    f"{db.select(from_table='users', where={'group_id': 1})}"
)

logger.info(
    f"All from users where group_id=4: "
    f"{db.select(from_table='users', where={'group_id': 4})}"
)

logger.info(
    f"Script for the last one: "
    f"{db.select(from_table='users', where={'group_id': 4}, execute=False)}"
)


####################################################
# SELECT data from DB
db.insertmany("users", [10, 1], [11, 2], [12, 3])
db.insertmany("users", [(20, 1), (21, 2), (23, 3)])
db.insertmany("users", [[30], [31, 2]])
db.insertmany("users", username=[41, 42, 43], group_id=[1, 2])

rem = ''
while rem.lower() not in ['y', 'n']:
    rem = input(f"\n\nAll tests passed! \nRemove {DB_NAME}?: ")
    if rem == 'y':
        remove(f"{getcwd()}/{DB_NAME}")


