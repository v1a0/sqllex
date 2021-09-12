# AbstractDatabase.create_table


```python
def create_table(
        self,
        name: AnyStr,
        columns: ColumnsType,
        IF_NOT_EXIST: bool = None,
        without_rowid: bool = None,
):
    """
    Method to create new table

    Parameters
    ----------
    name : AnyStr
        Name of creating table
    columns : ColumnsType
        Columns of table (ColumnsType-like)
    IF_NOT_EXIST :
        Turn on/off "IF NOT EXISTS" prefix
    without_rowid :
        Turn on/off "WITHOUT ROWID" postfix

    """
```

## Examples

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, TEXT, NOT_NULL, FOREIGN_KEY

db: AbstractDatabase = ...

db.create_table(
    'table',  # here is name of table
    {
        'column_1': INTEGER,
        'column_2': TEXT
    } 
)

db.create_table(
    'table2',  # here is name of table
    {
        'column_21': INTEGER,
        'column_22': TEXT
    },
    IF_NOT_EXIST=True
)

# database.db
#
# - table
# - - column_1
# - - column_2


db.create_table(
    name='books',
    columns={
        'id': [INTEGER],
        'name': [TEXT, NOT_NULL]
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
        'book_id': [INTEGER],
        'about': [TEXT, NOT_NULL],
        FOREIGN_KEY: {
            'book_id': ['books', 'id']
        }
    },
    IF_NOT_EXIST=True
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


### [Back to home](README.md)