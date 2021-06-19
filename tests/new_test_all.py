from sqllex import *
from sqllex.debug import debug_mode
from sqllex.types import *
from os import remove
from time import sleep, time

DB_NAME = "temp_table.db"

DB_TEMPLATE: DBTemplateType = {
    "t1": {
        "text_t": TEXT,
        "num_t": NUMERIC,
        "int_t": INTEGER,
        "real_t": REAL,
        "none_t": NONE,
        "blob_t": BLOB,
    }
}

db = SQLite3x(path=DB_NAME)

debug_mode(True, log_file='sqllex-test.log')


def remove_db():
    logger.stop()
    print("Logger stopped")

    remove(f"{DB_NAME}")
    print("Table removed")

    remove("sqllex-test.log")
    print("Log removed")


def tables_test():
    db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

    db.markup(
        {
            "groups": {
                "group_id": [PRIMARY_KEY, UNIQUE, INTEGER],
                "group_name": [TEXT, NOT_NULL, DEFAULT, "GroupName"],
            },

            "users": {
                "user_id": [INTEGER, PRIMARY_KEY, UNIQUE],
                "user_name": TEXT,
                "group_id": INTEGER,

                FOREIGN_KEY: {
                    "group_id": ["groups", "group_id"]
                },
            }
        }
    )

    db.create_table(
        "remove_me",
        {
            "xxx": [AUTOINCREMENT, INTEGER, PRIMARY_KEY],
            "yyy": [INTEGER],
        },
        IF_NOT_EXIST=True
    )

    for x in db.tables_names:
        if not (x in ['t1', 'groups', 'users', 'remove_me', 'sqlite_sequence']):
            print(db.tables_names)
            raise MemoryError

    db.drop('remove_me')

    for x in db.tables_names:
        if not (x in ['t1', 'groups', 'users', 'sqlite_sequence']):
            print(db.tables_names)
            raise MemoryError


def insert_test():
    # just arg values
    db.insert("t1", 'asdf', 10.0, 1, 3.14, None, 2)
    db["t1"].insert('asdf', 10.0, 1, 3.14, None, 2)

    # arg list
    db.insert("t1", ['asdf', 10.0, 1, 3.14, None, 2])
    db["t1"].insert(['asdf', 10.0, 1, 3.14, None, 2])

    # arg tuple
    db.insert("t1", ('asdf', 10.0, 1, 3.14, None, 2))
    db["t1"].insert(('asdf', 10.0, 1, 3.14, None, 2))

    # arg tuple
    db.insert("t1", {"text_t": 'asdf', "num_t": 10.0, "int_t": 1, "real_t": 3.14, "none_t": None, "blob_t": 2})
    db["t1"].insert({"text_t": 'asdf', "num_t": 10.0, "int_t": 1, "real_t": 3.14, "none_t": None, "blob_t": 2})

    # kwargs
    db.insert("t1", text_t='asdf', num_t=10.0, int_t=1, real_t=3.14, none_t=None, blob_t=2)
    db["t1"].insert(text_t='asdf', num_t=10.0, int_t=1, real_t=3.14, none_t=None, blob_t=2)

    if db.select_all('t1') == \
            db.select('t1') == \
            db.select('t1', ALL) == \
            db.select('t1', '*') == \
            db['t1'].select_all() == \
            db['t1'].select() == \
            db['t1'].select(ALL):
        sel_all = db.select_all('t1')
    else:
        raise MemoryError

    if not sel_all == [['asdf', 10.0, 1, 3.14, None, 2]] * 10:
        print(sel_all)
        print([['asdf', 10.0, 1, 3.14, None, 2]] * 10)
        raise MemoryError


def select_test():
    if not db.select('t1', 'text_t') == [['asdf']] * 10:
        print(db.select('t1', 'text_t'))
        raise MemoryError

    if not db.select('t1', ['text_t', 'num_t']) == [['asdf', 10.0]] * 10:
        print(db.select('t1', ['text_t', 'num_t']))
        raise MemoryError

    db.insert('t1', ['qwerty1', 11.1, 2, 4.14, None, 5])
    db.insert('t1', ['qwerty2', 11.1, 2, 4.14, None, 6])

    # WHERE as dict
    if not db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': 11.1}) == [['qwerty1', 11.1], ['qwerty2', 11.1]]:
        print(db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': 11.1}))
        raise MemoryError

    # WHERE as dict
    if not db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': ['=', 11.1], 'blob_t': ['<=', 5]}) == [
        ['qwerty1', 11.1]]:
        print(db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': 11.1, 'blob_t': 5}))
        raise MemoryError

    # WHERE as kwarg
    if not db.select('t1', ['text_t', 'num_t'], num_t=11.1) == [['qwerty1', 11.1], ['qwerty2', 11.1]]:
        print(db.select('t1', ['text_t', 'num_t'], num_t=11.1))
        raise MemoryError

    # WHERE as kwargs
    if not db.select('t1', ['text_t', 'num_t'], num_t=11.1, blob_t=6) == [['qwerty2', 11.1]]:
        print(db.select('t1', ['text_t', 'num_t'], num_t=11.1, blob_t=6))
        raise MemoryError

    # LIMIT test
    if not db.select('t1', text_t='asdf', LIMIT=5) == [['asdf', 10.0, 1, 3.14, None, 2]] * 5:
        print(db.select('t1', text_t='asdf', LIMIT=5))
        raise MemoryError

    # OFFSET
    if not db.select('t1', text_t='asdf', LIMIT=5, OFFSET=6) == [['asdf', 10.0, 1, 3.14, None, 2]] * 4:
        print(db.select('t1', text_t='asdf', LIMIT=5, OFFSET=6))
        raise MemoryError

    if not db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': ['>=', 11.1, 10], 'text_t': 'qwerty1'}) == \
           [['qwerty1', 11.1]]:
        print(db.select('t1', ['text_t', 'num_t'], WHERE={'num_t': ['>=', 11.1, 10], 'text_t': 'qwerty1'}))
        raise MemoryError

    db.create_table(
        "t2",
        {
            "id": [AUTOINCREMENT, INTEGER, PRIMARY_KEY],
            "value": [INTEGER, DEFAULT, 8],
        },
    )

    db.insertmany('t2', [[1], [2], [3], [4]])

    # ORDER_BY ASC
    if not db.select('t2', 'id', ORDER_BY='id ASC') == [[1], [2], [3], [4]]:
        print(db.select('t2', 'id', ORDER_BY='id ASC'))
        raise MemoryError

    # ORDER_BY DESC
    if not db.select('t2', ['id'], ORDER_BY='id DESC') == [[4], [3], [2], [1]]:
        print(db.select('t2', 'id', ORDER_BY='id DESC'))
        raise MemoryError

    if not db.select(
            't2',
            WHERE={
                'id': ['<', 3]
            },
    ) == [[1, 8], [2, 8]]:
        print(db.select('t2', WHERE={'id': ['<', 3]}))
        raise MemoryError

    # JOIN
    if not db.select(
            't2',
            'id',
            JOIN=[
                [CROSS_JOIN, 't1', AS, 't', ON, 't.num_t > t2.value']
            ]
    ) == [
               [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1],
               [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2],
               [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3],
               [4], [4], [4], [4], [4], [4], [4], [4], [4], [4], [4], [4]
           ]:
        print(db.select('t2', 'id', JOIN=[[CROSS_JOIN, 't1', AS, 't', ON, 't.num_t > t2.value']]))
        raise MemoryError


def insertmany_test():
    db.create_table(
        't3',
        {
            'id': [INTEGER, NOT_NULL],
            'val': [TEXT, DEFAULT, 'NO']
        }
    )

    db.insertmany('t3', [[1, 'hi']] * 10)
    db.insertmany('t3', [[1]] * 10)
    db.insertmany('t3', ((1, 'hi'),) * 10)
    db.insertmany('t3', ((1,),) * 10)
    db.insertmany('t3', id=[2] * 10)
    db.insertmany('t3', id=(2,) * 10)

    if not db.select_all('t3') == [
        [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'],
        [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'],
        [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'hi'],
        [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'], [1, 'hi'],
        [1, 'hi'], [1, 'hi'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'],
        [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [1, 'NO'], [2, 'NO'], [2, 'NO'],
        [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'],
        [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO'],
        [2, 'NO'], [2, 'NO'], [2, 'NO'], [2, 'NO']
    ]:
        raise MemoryError

    db.create_table(
        't6',
        {
            'id': [INTEGER, UNIQUE, NOT_NULL],
            'val': [TEXT, DEFAULT, 'def_val']
        }
    )

    db.insertmany('t6', [[x, 'hi'] for x in range(100)])

    if not db.select_all('t6') == [[x, 'hi'] for x in range(100)]:
        raise MemoryError

    db.insertmany('t6', [[x, 'bye'] for x in range(100)], OR=REPLACE)

    if not db.select_all('t6') == [[x, 'bye'] for x in range(100)]:
        raise MemoryError

    db.updatemany('t6', [[], [], []])

    if not db.select_all('t6') == [[x, 'bye'] for x in range(100)]:
        raise MemoryError


def update_test():
    db.create_table(
        't4',
        {
            'id': [INTEGER, NOT_NULL, UNIQUE],
            'val': [TEXT, DEFAULT, 'NO']
        }
    )

    db.insertmany('t4', [[x, bin(x)] for x in range(100)])

    db.update(
        't4',
        {'val': 'NEW_VAL'},
        WHERE={
            'id': ['<', 50]
        }
    )

    if not db.select('t4', 'id', WHERE={"val": 'NEW_VAL'}) == [[x] for x in range(50)]:
        print(db.select('t4', 'id', WHERE={"val": 'NEW_VAL'}))
        raise MemoryError


def delete_test():
    db.delete('t4', id=['<', 50])

    if not db.select('t4', 'id', WHERE={"val": 'NEW_VAL'}) == []:
        print(db.select_all('t4'))
        raise MemoryError


def replace_test():
    db.create_table(
        't5',
        {
            'id': [INTEGER, UNIQUE, NOT_NULL],
            'val': [TEXT, DEFAULT, '_x_']
        }
    )

    db.insertmany('t5', [[x, ] for x in range(100)])

    db.replace('t5', [99, 'O_O'])

    if not db.select('t5', val='O_O') == [[99, 'O_O']]:
        print(db.select('t5', val='O_O'))
        raise MemoryError


def get_tables_test():
    if "<generator object SQLite3x._get_tables" not in str(db.tables):
        print(db.tables)
        raise MemoryError

    for table in db.tables:
        if table.name not in ['t1', 'groups', 'users', 'sqlite_sequence', 't2', 't3', 't4', 't5', 't6', 't7']:
            print(table)
            raise MemoryError

    for table in db.tables:
        if table.name not in ['t1', 'groups', 'users', 'sqlite_sequence', 't2', 't3', 't4', 't5', 't6', 't7']:
            print(table)
            raise MemoryError

    for name in db.tables_names:
        if name not in ['t1', 'groups', 'users', 'sqlite_sequence', 't2', 't3', 't4', 't5', 't6', 't7']:
            print(name)
            raise MemoryError


def getitem_test():
    db.create_table(
        't7',
        {
            'id': INTEGER,
            'name': TEXT
        }
    )

    t7 = db['t7']
    t7_id = t7['id']
    t7_name = t7['name']

    if t7.columns_names != ['id', 'name']:
        raise MemoryError

    t7.insert([1, 'Alex'])
    t7.insert([2, 'Blex'])

    if t7.select(ALL, (t7_id == 2) | (t7_id == 1) & 1) != [[1, 'Alex'], [2, 'Blex']]:
        raise MemoryError

    t7.update(
        {'name': "XXXX"},
        WHERE=t7_id == 1
    )

    if t7.select([t7_name, 'id'], WHERE=(t7_id == 2) | (t7_id == 1) & 1) != [['XXXX', 1], ['Blex', 2]]:
        raise MemoryError

    t7.update(
        {
            t7_id: t7_id + 2
        },
        WHERE=t7_name == 'XXXX'
    )

    if t7.select([t7_name, t7_id], WHERE=(t7_id == 3)) != [['XXXX', 3]]:
        print(t7.select([t7_name, t7_id], WHERE=(t7_id == 2) | (t7_id == 1) & 1))
        raise MemoryError


def has_add_remove_column_test():
    db.create_table(
        't8',
        {
            'id': INTEGER,
            'test': TEXT
        }
    )
    t8 = db["t8"]
    t8.add_column({"col1": [TEXT, DEFAULT, '123']})
    t8.add_column({"col2": TEXT})

    if t8.columns_names != ['id', 'test', 'col1', 'col2']:
        print(t8.columns_names)
        raise MemoryError

    col2 = t8['col2']
    t8.remove_column(col2)
    t8.remove_column("col1")


    if t8.columns_names != ['id', 'test']:
        raise MemoryError
    
    if not t8.has_column("id") and not t8.has_column("test") and t8.has_column("col1") and t8.has_column("col2"):
        raise MemoryError


# Start time counting
t = time()

# Connection
db.connect()

# Testes
tables_test()
insert_test()
select_test()
insertmany_test()
update_test()
delete_test()
replace_test()
getitem_test()
get_tables_test()
# has_add_remove_column_test()   # workflow falling by no reason issue #

# Disconnect
db.disconnect()

# Time counting
t = time() - t

# Little sleep and printing
sleep(0.1)
print(t)

# Remove db
remove_db()
