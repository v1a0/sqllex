# SQLite3x.execute

```python
def execute(
        self,
        script: AnyStr = None,
        values: Tuple = None,
        request: SQLRequest = None
) -> Union[List, None]:
    """
    Execute any SQL-script whit (or without) values, or execute SQLRequest
    Parameters
    ----------
    script : AnyStr
        single SQLite script, might contains placeholders
    values : Tuple
        Values for placeholders if script contains it
    request : SQLRequest
        Instead of script and values might execute full statement
    Returns
    ----------
    Union[List, None]
        Database answer if it has
    """
```


## Examples

```python

from sqllex import *

db = SQLite3x(path='database.db')

db.execute(
    script="""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY UNIQUE,
        name TEXT
    )
    """
)

db.execute(
    script="""
    INSERT INTO users (id, text) VALUES (?, ?)
    """,
    values=(1, 'Alex')
)


request = {
    'script': "INSERT INTO users (id, text) VALUES (?, ?)",
    'values': (2, 'Bob')
}

db.execute(**request)

```

### [Back to home](README.md)