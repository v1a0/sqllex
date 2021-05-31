from sqllex import *

db = SQLite3x(path='database.db')

db.markup({
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

users_table = db['users']   # get table as object
ut2 = db['users2']   # get table as object

ut2.insert(1, 'A')
ut2.insert(2, 'B')
ut2.update(SET={'username': 'new_uname'})

print(users_table.columns)  # ['id', 'username']

users_table.insert(1, "New_user")   # insert new record in table

print(users_table.select())
print(ut2.select())


# Issue #19
#
# File "main.py", line 9, in <module>
#     detectives = db["detectives"]
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 931, in __getitem__
#     return SQLite3xTable(db=self, name=key)
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 653, in __init__
#     self.columns = self.get_columns()
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 685, in get_columns
#     return self.db.get_columns(table=self.name)
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 1582, in get_columns
#     columns = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 1390, in execute
#     return self._execute_stmt_(script=script, values=values, request=request)
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 566, in t2l_wrapper
#     ret = lister(func(*args, **kwargs))
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 405, in execute_wrapper
#     ret_ = executor(conn, stmt)
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 382, in executor
#     raise error
#   File "/usr/local/lib/python3.8/site-packages/sqllex/classes/sqlite3x.py", line 377, in executor
#     cur.execute(stmt.request.script)
# sqlite3.OperationalError: no such table: PRAGMA_TABLE_INFO