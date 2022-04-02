# Column

Sub-class of AbstractTable, itself it's one abstract column inside abstract table.
Primary have the same methods but without table name argument.

```python
class AbstractColumn:
    """
    Sub-class of AbstractTable, itself it's one abstract column inside of abstract table
    Primary have the same methods but without table name argument

    This class existing for generating SearchConditions
    in constructions like this:
        db['table_name']['column_name'] = x
        db['table_name']['column_name'] > x
        db['table_name']['column_name'] >= x
        db['table_name']['column_name'] != x
        ...
        db['table_name']['column_name'] / x

        AND SPECIAL: column-like-reg_ex
        db['table_name']['column_name'] |LIKE| '%find_me%'
    """

    def __init__(self, table: str, name: AnyStr, placeholder='?'):
        """
        Attributes
        ----------
        table : AbstractTable
            Parent table object
        name : str
            Name of column
        placeholder : str
            Symbol used in scripts as placeholder

        """
```


# Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='db-1.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER, sx.PRIMARY_KEY, sx.UNIQUE],
        'name': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, 'Unknown']
    }
)

id_col: sx.SQLite3xColumn = db['users']['id']  # AbstractColumn
name_col: sx.SQLite3xColumn = db['users']['name']  # AbstractColumn

db.update(
    TABLE='users',  # table name
    SET=['username', 'Updated_name_0'],  # set username 'Updated_name_0'
    WHERE=(
            id_col == 1  # where id == 1
    )
)

db.update(
    'users',  # table name
    ['username', 'Updated_name_1'],  # set username 'Updated_name_1'
    id_col > 1  # where id > 1
)

db.update(
    'users',
    SET={
        'name': 'Updated_name_1'
    },
    WHERE=(
            id_col == 1
    )
)

db.update(
    'users',
    SET={
        name_col: name_col + '__UPDATED'  # SET id column name value == old value + '__UPDATED'
    },
    WHERE=(
            id_col == 1
    )
)

```


### [Back to home](README.md)