# AbstractDatabase.markup


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
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, TEXT, NOT_NULL, FOREIGN_KEY

db: AbstractDatabase = ...

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
            'id': [INTEGER],
            'name': [TEXT, NOT_NULL]
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
            'book_id': [INTEGER],
            'about': [TEXT, NOT_NULL],
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
            'c1': [INTEGER],
            'c2': [TEXT, NOT_NULL],
        },
        'table_2': {
            'c1': [INTEGER],
        },
        'table_3': {
            'c1': [INTEGER],
        },
    }
)

```


### [Back to home](README.md)