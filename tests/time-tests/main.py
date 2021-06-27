import cProfile
import pstats
from sqllex import *


def init_db():
    db = SQLite3x('time_test.db')


def crete_table(db: SQLite3x):
    db.create_table(
        'main',
        {
            'id': [INTEGER, PRIMARY_KEY, UNIQUE],
            'name': [TEXT],
            'age': [INTEGER, DEFAULT, 33]
        }
    )


def insert_fats(db: SQLite3x):
    for _ in range(1000):
        db.insert('main', [None, f'Alex', 33])


def insert_slow(db: SQLite3x):
    for _ in range(1000):
        db.insert('main', [None, 'Alex'])


def insert_many_fast(db: SQLite3x):
    data = [[None, 'Alex', 33] for _ in range(1000)]

    db.insertmany('main', data)


def insert_many_slow(db: SQLite3x):
    data = [[None, 'Alex'] for _ in range(1000)]

    db.insertmany('main', data)


def select_all(db: SQLite3x):
    db.select_all('main', LIMIT=1000)


def select_where_1(db: SQLite3x):
    db.select(
        'main', 'id',
        WHERE={
            'name': 'Alex'
        },
        LIMIT=1000
    )


def select_where_2(db: SQLite3x):
    """
    Modern new way to
    """
    main_tab = db['main']
    id_col = main_tab['id']
    name_col = main_tab['name']

    db.select(
        main_tab, id_col,
        WHERE=(name_col == 'Alex'),
        LIMIT=1000
    )


if __name__ == '__main__':
    db = SQLite3x('time_test.db')

    db.connect()

    with cProfile.Profile() as pr:
        # crete_table(db)       # 0.003847
        # insert_fats(db)       # 0.06685 sec (1000 rec)
        # insert_slow(db)       # 0.2699 sec  (1000 rec)
        # insert_many_fast(db)  # 0.005199    (1000 rec)
        # insert_many_slow(db)  # 0.005518    (1000 rec)
        # select_all(db)        # 0.005709    (1000 rec)
        # select_where_1(db)    # 0.002922    (1000 rec)
        # select_where_2(db)    # 0.003836    (1000 rec) << why?
        pass

    db.disconnect()

    stat = pstats.Stats(pr)
    stat.sort_stats(pstats.SortKey.TIME)
    stat.dump_stats(filename='time_tst.prof')


# RESULTS
# 0.002004 = listers.py:5(lister)
# LISTER TAKES HALF OF ALL TIME IN SELECT-LIKE METHODS
#
# 0.000353
# <built-in method builtins.isinstance> takes 1/10 of all time
#
#
