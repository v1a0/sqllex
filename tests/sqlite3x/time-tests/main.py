import cProfile
import pstats
from sqllex import *
from sqllex.debug import debug_mode

LIM = 10000


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
    for _ in range(LIM):
        db.insert('main', (None, f'Alex', 33))


def insert_slow(db: SQLite3x):
    for _ in range(LIM):
        db.insert('main', (None, 'Alex'))


def insert_many_fast(db: SQLite3x):
    data = [(None, 'Alex', 33) for _ in range(LIM)]

    db.insertmany('main', data)


def insert_many_slow(db: SQLite3x):
    data = [(None, 'Alex') for _ in range(LIM)]

    db.insertmany('main', data)


def select_all(db: SQLite3x):
    db.select_all('main', LIMIT=LIM)


def select_where_1(db: SQLite3x):
    db.select(
        'main', 'id',
        WHERE={
            'name': 'Alex'
        },
        LIMIT=LIM
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
        LIMIT=LIM
    )


if __name__ == '__main__':
    db = SQLite3x('time_test.db')

    db.connect()

    with cProfile.Profile() as pr:
        #                     # total runtime/(records) 0.2.0.0-rc4
        #                     # all == 0.651 sec (1.03x)
        crete_table(db)       # 0.00333 sec/(1    table),
        insert_fats(db)       # 0.194000 sec/(10_000 rec),
        insert_slow(db)       # 0.68840 sec/(10_000 rec),
        insert_many_fast(db)  # 0.03620 sec/(10_000 rec),
        insert_many_slow(db)  # 0.03409 sec/(10_000 rec),
        select_all(db)        # 0.01042 sec/(10_000 rec),
        select_where_1(db)    # 0.00680 sec/(10_000 rec),
        select_where_2(db)    # 0.00706 sec/(10_000 rec),
        pass

    db.disconnect()

    stat = pstats.Stats(pr)
    stat.sort_stats(pstats.SortKey.TIME)
    stat.dump_stats(filename='time_tst.prof')

