from sqllex import *
from time import time

path = 'my_awesome_db.db'

# Init-ing your databse
db = SQLite3x(path='my_awesome_db.db')

db.create_table(
    name='users',  # here is name of table
    columns={
        'id': [INTEGER, PRIMARY_KEY],  # user id
        'username': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],  # user name
    },
    IF_NOT_EXIST=True
)

t = time()

db.connect()

users = db['users']

# users.insertmany(
#     [
#         [1, '12'],
#     ]
# )

import time
import sqlite3
import sqllex

sqllex.debug.debug_mode(False)


def bench_sqllex():
    db = sqllex.SQLite3x('db-1')
    db.connect()
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(1000):
        db.insert("numbers", i, execute=False)
    db.disconnect()


def bench_sqlite3():
    with sqlite3.connect('db-2') as db:
        db.execute("CREATE TABLE numbers (value INTEGER)")
        for i in range(1000):
            db.execute("INSERT INTO numbers (value) VALUES (?)", (i,))


beg = time.time()
bench_sqllex()
end = time.time()
print(f"sqllex\t{end - beg:.3}s")

beg = time.time()
bench_sqlite3()
end = time.time()
print(f"sqlite3\t{end - beg:.3}s")
