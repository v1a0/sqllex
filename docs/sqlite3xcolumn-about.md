# SQLite3xColumn

```python
class SQLite3xColumn:
    """
    Sub-class of SQLite3xTable, itself one column of table (SQLite3xTable)
    Have same methods but without table name argument
    Attributes
    ----------
    table : SQLite3xTable
        SQLite3xTable parent table object
    name : str
        Name of column
    
    Existing for generating SQLite3xSearchCondition for WHERE, SET
    and other parameters of parents classes
    
    db['table_name']['column_name'] = x
    db['table_name']['column_name'] > x
    db['table_name']['column_name'] >= x
    db['table_name']['column_name'] != x
    ...
    db['table_name']['column_name'] / x
    """
```

# Magic methods
```python
def __str__(self):
    return f"'{self.table.name}'.'{self.name}'"

def _str_gen(self, value, operator: str):
    if type(value) == str:
        return SQLite3xSearchCondition(
            f"({self}{operator}'{value}')"  # unsafe!
        )
    else:
        return SQLite3xSearchCondition(
            f"({self}{operator}{value})"
        )

def __lt__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '<')

def __le__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '<=')

def __eq__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '=')

def __ne__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '<>')

def __gt__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '>')

def __ge__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '>=')

def __add__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '+')

def __sub__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '-')

def __mul__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '*')

def __truediv__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '/')

def __divmod__(self, value) -> SQLite3xSearchCondition:
    return self._str_gen(value, '%')

def __list__(self) -> List[Any]:
    return self.table.select_all(self.name)

def __hash__(self):
    return hash(f"'{self.name}'.'{self.table}'")
```

# Examples

```python
from sqllex import *
from sqllex.classes import SQLite3xColumn

db = SQLite3x(path='database.db')

db.create_table(
    'users',
    {
        'id': [INTEGER, PRIMARY_KEY, UNIQUE],
        'name': [TEXT, NOT_NULL, DEFAULT, 'Unknown']
    }
)


id_col: SQLite3xColumn = db['users']['id']  # SQLite3xColumn
name_col: SQLite3xColumn = db['users']['name']  # SQLite3xColumn


db.update(
    TABLE='users',                            # table name
    SET=['username', 'Updated_name_0'],       # set username 'Updated_name_0'
    WHERE=(
            id_col == 1                       # where id == 1
    )
)


db.update(
    'users',                            # table name
    ['username', 'Updated_name_1'],     # set username 'Updated_name_1'
    id_col > 1                          # where id > 1
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
        name_col: name_col + '__UPDATED'    # SET id column name value == old value + '__UPDATED'
    },
    WHERE=(
        id_col == 1
    )
)

```


### [Back to home](README.md)