<div align="center">

# SQLite3x.execute

</div><br>

## About

Method to execute SQL script

```python
def execute(self,
            script: AnyStr,
            values: tuple = None,
            request: SQLRequest = None
            ) -> Union[List, None]:
```

>:param script: single SQLite script, might contains placeholders

>:param values: Values for placeholders if script contains it

>:param request: Instead of script and values might execute full statement

>:return: Database answer if it has


## Examples

```python

from sqllex import *
from sqllex.types import SQLRequest

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


request = SQLRequest(
    script="""
    INSERT INTO users (id, text) VALUES (?, ?)
    """,
    values=(2, 'Bob')
)

db.execute(request=request)

```

Read also:
- SQLite3x.executemany