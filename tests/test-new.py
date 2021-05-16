from sqllex import SQLite3x, INTEGER, PRIMARY_KEY, UNIQUE, TEXT, NOT_NULL, DEFAULT, FOREIGN_KEY, REPLACE, AUTOINCREMENT
from sqllex.debug import debug_mode


def test(d):
    table = d["nums"]
    table.select_all()


debug_mode(False)

DB_NAME = "test_table1.db"

DB_TEMPLATE = {
    "nums": {
        "id": INTEGER
    }
}

db = SQLite3x(path=DB_NAME, template=DB_TEMPLATE)

db.connect()
test(db)

print(db.connection)

db.disconnect()

print(db.connection)
