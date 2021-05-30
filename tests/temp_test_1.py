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
