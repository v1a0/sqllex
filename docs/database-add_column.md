# SQLite3x.add_column

```python
def add_column(
        self,
        table: AnyStr,
        column: ColumnsType
) -> None:
    """
    Adds column to the table

    Parameters
    ----------
    table : AnyStr
        Name of table
    column : ColumnType
        Columns of table (ColumnsType-like)
        ColumnType name and SQL type e.g. {'value': INTEGER}

    Returns
    ----------
    None
    """
```

# Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER, sx.PRIMARY_KEY, sx.UNIQUE],
        'name': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, 'Unknown']
    }
)

print(db.get_columns_names('users'))  # ['id', 'name']

db.add_column(
    'users', 
    {
        'group': [sx.INTEGER, sx.NOT_NULL]
    },
)

print(db.get_columns_names('users'))  # ['id', 'name', 'group']

```

### [Back to home](README.md)