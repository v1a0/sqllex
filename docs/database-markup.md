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
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.markup(
    template={
        'table': {
            'column_1': sx.INTEGER,
            'column_2': sx.TEXT
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
            'id': [sx.INTEGER],
            'name': [sx.TEXT, sx.NOT_NULL]
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
            'book_id': [sx.INTEGER],
            'about': [sx.TEXT, sx.NOT_NULL],
            sx.FOREIGN_KEY: {
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
            'c1': [sx.INTEGER],
            'c2': [sx.TEXT, sx.NOT_NULL],
        },
        'table_2': {
            'c1': [sx.INTEGER],
        },
        'table_3': {
            'c1': [sx.INTEGER],
        },
    }
)

```


### [Back to home](README.md)