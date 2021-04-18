<div align="center">

# SQLite3x.markup

</div><br>

## About

Method to INSERT many values into db's table. Same as [SQLite3x.create_table](https://github.com/V1A0/sqllex/wiki/SQLite3x.create_table)


```python
def markup(self,
           template: DBTemplateType
           ):
```


> :param template: Structure of database (DBTemplateType)



## Examples

```python

from sqllex import *

db = SQLite3x(path='database.db')

db.markup(
    template={
        'table': {
            'column_1': INTEGER,
            'column_2': TEXT
        } 
    }
)

# database.db
#
# - table
# - - column_1
# - - column_2


db.markup(
    template={
        'books': {
            'id': [INTEGER, PRIMARY_KEY, UNIQUE],
            'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
        } 
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


db.markup(
    template={
        'descriptions': {
            'book_id': [INTEGER, PRIMARY_KEY, UNIQUE],
            'about': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
            FOREIGN_KEY: {
                'book_id': ['books', 'id']
            }
        } 
    }
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