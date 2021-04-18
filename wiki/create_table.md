<div align="center">

# SQLite3x.create_table

</div><br>

## About

Method to CREATE TABLE, same as [SQLite3x.markup](https://github.com/V1A0/sqllex/wiki/SQLite3x.markup)

Optional:

> CREATE TABLE (IF NOT EXISTS) schema-name.table-name (AS select-stmt) / (column-def table-constraint) (WITHOUT ROWID)


```python
def create_table(self,
                 name: AnyStr,
                 columns: ColumnsType,
                 if_not_exist: bool = None,
                 as_: SQLRequest = None,
                 without_rowid: bool = None
                 ):
```

>:param name: Table name

>:param columns: Columns of table (ColumnsType)

>:param if_not_exist: Turn on/off "IF NOT EXISTS" prefix

>:param as_:

>:param without_rowid:

>:param execute: Execute script and return db's answer (True) or return script (False)



## Examples

```python

from sqllex import *

db = SQLite3x(path='database.db')

db.create_table(
    'table',  # here is name of table
    {
        'column_1': INTEGER,
        'column_2': TEXT
    } 
)

# database.db
#
# - table
# - - column_1
# - - column_2


db.create_table(
    name='books',
    columns={
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
    } 
)

# database.db
#
# - table
# - - column_1
# - - column_2
#
# - books
# - - id
# - - name


db.create_table(
    name='descriptions',
    columns={
        'book_id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'about': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        FOREIGN_KEY: {
            'book_id': ['books', 'id']
        }
    },
    if_not_exist=True
)


# database.db
#
# - table
# - - column_1
# - - column_2
#
# - books
# - - id  <─────────┐
# - - name          │
#                   │ FOREIGN_KEY
# - descriptions    │
# - - book_id >─────┘
# - - about


```

Read also:
- SQLite3x.create_table