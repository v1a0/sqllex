import time
import sqlite3
import sqllex

sqllex.debug.debug_mode(False)


def bench_sqllex_connect():
    db = sqllex.SQLite3x('db-1.db')
    db.connect()
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(10000):
        # t = time.time()
        db.insert("numbers", i)
        # if time.time() - t > 0: print(time.time() - t, i) # 0.0020232200622558594 974
    db.disconnect()


def bench_sqllex_without_connect():
    db = sqllex.SQLite3x('db-2.db')
    db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)
    for i in range(10000):
        db.insert("numbers", i)


def bench_sqlite3():
    with sqlite3.connect('db-3.db') as db:
        db.execute("CREATE TABLE numbers (value INTEGER)")
        for i in range(10000):
            # t = time.time()
            db.execute("INSERT INTO numbers (value) VALUES (?)", (i,))
            # if time.time() - t > 0: print(time.time()-t, i)


print("\nRunning sqllex_connect")
beg = time.time()
bench_sqllex_connect()
end = time.time()
print(f"sqllex_connect\t{end - beg:.3}s")   # sqllex_connect (v0.1.10.4 = 0.123s) vs (v0.1.10.3b = 0.445 sec) (3.3969x)

print("\nRunning sqllex_without_connect")
beg = time.time()
bench_sqllex_without_connect()
end = time.time()
print(f"sqllex_without_connect\t{end - beg:.3}s")    # sqllex_without_connect (v0.1.10.4 = 45.4s) vs (.3b = 0.461 sec)

print("\nRunning sqlite3")
beg = time.time()
bench_sqlite3()
end = time.time()
print(f"sqlite3\t{end - beg:.3}s")  # sqlite3	0.0308s
