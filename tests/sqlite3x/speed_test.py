import time
import sqlite3
import sqllex


sqllex.debug.debug_mode(False)

COMPLEXITY = 10_000


def time_rec(func: callable):
    def wrapper_time_rec(*args, **kwargs):
        print(f"\n{func.__name__}, result=", end='\r')
        beg = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}, result={end - beg:.3}s")

    return wrapper_time_rec


@time_rec
def bench_sqllex_default():
    db = sqllex.SQLite3x('db-1.db')
    db.connect()
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(COMPLEXITY):
        db.insert("numbers", i)
    db.disconnect()


@time_rec
def bench_sqllex_without_connect():
    db = sqllex.SQLite3x('db-2.db')
    db.disconnect()
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(COMPLEXITY):
        db.insert("numbers", i)


@time_rec
def bench_raw_sqlite3():
    with sqlite3.connect('db-3.db') as db:
        db.execute("CREATE TABLE numbers (value INTEGER)")
        for i in range(COMPLEXITY):
            db.execute("INSERT INTO numbers (value) VALUES (?)", (i,))


@time_rec
def branch_fast_insert_sqllex():
    db = sqllex.SQLite3x('db-4.db')
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    db.insertmany("numbers", ((i,) for i in range(COMPLEXITY)))



@time_rec
def branch_fast_insert_raw_sqlite():
    with sqlite3.connect('db-5.db') as db:
        db.execute("CREATE TABLE numbers (value INTEGER)")
        db.executemany("INSERT INTO numbers (value) VALUES (?)", ((i,) for i in range(COMPLEXITY)))


if __name__ == '__main__':
    bench_sqllex_default()
    # v0.1.10.3b = 0.445s
    # v0.1.10.4 = 0.123s
    # v0.2.0.0-rc4 = 0.108s (4.12x faster than 0.1.10.3b)

    bench_raw_sqlite3()
    # sqlite3 = 0.0303s


    print('\n', '-\t'*10)


    branch_fast_insert_sqllex()
    # v0.1.10.3b = 0.145 sec
    # v0.1.10.4 = 0.0266s
    # v0.2.0.0-rc4 = 0.0264s (5.49x faster than 0.1.10.3b)

    branch_fast_insert_raw_sqlite()
    # sqlite3	0.0179s

    print('\n', '-\t'*10)

    # bench_sqllex_without_connect()
    # v0.1.10.3b = 46.1s
    # v0.1.10.4 = 45.4s
    # v0.2.0.0-rc4 = 46.7s
