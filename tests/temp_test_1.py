# import all from sqllex package
from sqllex import *

# Create database file 'database.db'
db = SQLite3x(path='database.db')

# Create table inside database
db.create_table(
    'users',
    {
        'id': [INTEGER, UNIQUE],
        'username': TEXT
    }
)
