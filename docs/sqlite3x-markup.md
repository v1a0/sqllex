# SQLite3x.markup


```python
def markup(
        self,
        template: DBTemplateType
):
    """
    Mark up table structure from template
    Parameters
    ----------
    template : DBTemplateType
        Template of database structure (DBTemplateType-like)
    """
```

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


db.markup(
    template={
        'table_1': {
            'c1': [INTEGER, PRIMARY_KEY],
            'c2': [TEXT, NOT_NULL, DEFAULT, 'Unknown'],
        },
        'table_2': {
            'c1': [INTEGER, PRIMARY_KEY],
        },
        'table_3': {
            'c1': [INTEGER, PRIMARY_KEY],
        },
    }
)

```


### [Back to home](./index.md)