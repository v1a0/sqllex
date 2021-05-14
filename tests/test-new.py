import time
import sqlite3
import sqllex

sqllex.debug.debug_mode(True)


def bench_sqllex_connect():
    db = sqllex.SQLite3x('db-1')
    db.connect()
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(1000):
        db.insert("numbers", i)
    db.disconnect()


def bench_sqllex_without_connect():
    db = sqllex.SQLite3x('db-2')
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(1000):
        db.insert("numbers", i, execute=False)


def bench_sqlite3():
    with sqlite3.connect('db-3') as db:
        db.execute("CREATE TABLE numbers (value INTEGER)")
        for i in range(1000):
            db.execute("INSERT INTO numbers (value) VALUES (?)", (i,))


beg = time.time()
bench_sqllex_connect()
end = time.time()
print(f"sqllex_connect\t{end - beg:.3}s")

beg = time.time()
#bench_sqllex_without_connect()
end = time.time()
print(f"sqllex_without_connect\t{end - beg:.3}s")

beg = time.time()
bench_sqlite3()
end = time.time()
print(f"sqlite3\t{end - beg:.3}s")
