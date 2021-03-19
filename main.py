from src import *

db_template = {
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


db = SQL3X(template=db_template)
db.insert("groups", group_id=1, name="Admins")
db.insert("groups", group_id=2, name="Other")

import time
_t = time.time()
db.insert("users", username="user_1", group_id=1)
db.insert("users", "user_2", 1)
db.insert("users", ["user_3", 2])
db.insert("users", ("user_4", 2))
db.insert("users", {'username': "user_4", 'group_id': 2})
print(time.time() - _t)


# db.select(['contact_id', 'group_id'], from_table='contact_groups', where={'contact_id': 1})
