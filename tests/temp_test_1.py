from sqllex import *
from time import time


def test1():
    db_ = SQLite3x(path='database.db')

    db_.markup({
        'users':
            {
                'id': [INTEGER, UNIQUE],
                'username': TEXT
            },
        'users2':
            {
                'id': [INTEGER, UNIQUE],
                'username': TEXT
            }
    }
    )

    users_table = db_['users']  # get table as object
    ut2 = db_['users2']  # get table as object

    ut2.insert(1, 'A')
    ut2.insert(2, 'B')
    ut2.update(SET={'username': 'new_uname'})

    print(users_table.columns)  # ['id', 'username']

    users_table.insert(1, "New_user")  # insert new record in table

    print(users_table.select())
    print(ut2.select())

    print(db_.select(SELECT=ALL, FROM="users", LIMIT=10))


def temp2():
    db = SQLite3x(path='test.db')

    db.connect()

    db.create_table(
        't6',
        {
            'id': [INTEGER, UNIQUE, NOT_NULL],
            'val': [TEXT, DEFAULT, 'def_val']
        },
        IF_NOT_EXIST=True
    )

    data1 = [[x, 'hi'] for x in range(100_000)]
    data2 = [[x, 'bye'] for x in range(100_000)]

    t = time()

    db.insertmany('t6', data1)

    print(time() - t)  # 0.273134708404541 sec - insert 100,000 values

    t = time()

    db.insertmany('t6', data2, OR=REPLACE)

    print(time() - t)  # 0.31252258110046387 sec - update 100,000 values

    t = time()

    db.updatemany('t6', data2)

    print(time() - t)  # 0.31252258110046387 sec - update 100,000 values


i = {
    'MAIN': {
        'METHOD': "select",
        'SELECT': [[]],
        'WHERE': []
    },
    'WITH': None,
    'ORDER_BY': None,
    'LIMIT': 10,
    'OFFSET': None,
    'JOIN': None,
}

db = SQLite3x(path='test.db')

db.connect()

print(db.path)


db.create_table(
    'users',
    {
        'id': [INTEGER, UNIQUE, NOT_NULL],
        'first_name': [TEXT, NOT_NULL],
        'second_name': [TEXT, NOT_NULL],
        'age': INTEGER
    }
)

from datetime import datetime

uid = 1
first_name = "Alex"
second_name = "Flex"
age = 33

db.insert(
    'users',
    uid,
    first_name=first_name,
    second_name=second_name,

)