<div align="center">

# SQLite3x.executemany

</div><br>

## About

Method to execute many SQL scripts

```python
def executemany(self,
                script: AnyStr,
                values: tuple = None,
                request: SQLRequest = None
                ) -> Union[List, None]:
```


>:param script: single or multiple SQLite script(s), might contains placeholders

>:param values: Values for placeholders if script contains it

>:param request: Instead of script and values might execute full request

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

db.executemany(
    script="""
    INSERT INTO users (id, text) VALUES (?, ?)
    """,
    values=((1, 'Alex'), (2, 'Bob'))
)


request = SQLRequest(
    script="""
    INSERT INTO users (id, text) VALUES (?, ?)
    """,
    values=((3, 'Cate'), (4, 'Dex'))
)

db.executemany(request=request)

```

Read also:
- SQLite3x.executemany