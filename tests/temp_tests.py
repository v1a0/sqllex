import sqllex as sx
from sqllex.core.entities.abc.sql_transaction import Transaction

db = sx.SQLite3x(':memory:')

tran = Transaction(db)

with tran as t:
    print(t)


with tran as t:
    print(t.dsf)
