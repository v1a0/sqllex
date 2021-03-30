from sqllex import SQLite3x, INTEGER, PRIMARY_KEY, UNIQUE, TEXT, NOT_NULL, DEFAULT, FOREIGN_KEY, ExecuteError, REPLACE
from os import walk, getcwd, remove
from loguru import logger


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


db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

# db.insert("groups", group_id=1, name="Admins")
# db.insert("groups", group_id=2, name="Other")

db.insert("users", ["user_1", 1]) # kwargs.get('data')
db.insert("users", ("user_2", 2))
db.insert("users", "user_3", 2)
db.insert("users", username="user_4", group_id=1)
db.insert("users", username="user_5")
db.insert("users", {
   'username': "user_6",
   'group_id': 1
})
#db.insert(
#   table="users",
#   {'username': "user_6",
#   'group_id': 1
#}, WITH=)

db.replace("users", ["user_1", 5])


db.insert("users", username="user_4", group_id=1,
          OR=REPLACE,
          WITH={
              'a': db.select(
                  from_table='users',
                  where={'group_id': 1},
                  execute=False
              )}
          )


db.insert("users", username="user_4", group_id=1,
          OR=REPLACE,
          WITH={
              'a': "SELECT * FROM users WHERE (group_id=2)"
          })