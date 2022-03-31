# SQLite3x.executemany

```python
def executemany(
        self,
        script: AnyStr = None,
        values: Tuple[Tuple] = None,
) -> Union[Tuple, None]:
    """
    Execute any SQL-script for many values sets
    
    Parameters
    ----------
    script : AnyStr
        single or multiple SQLite script(s), might contains ph_amount
    values : Tuple[Tuple]
        Values for ph_amount if script contains it
    
    Returns
    ----------
    Union[Tuple, None]
        ABDatabase answer if it has
    """
```


## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

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


request = {
    'script': "INSERT INTO users (id, text) VALUES (?, ?)",
    'values': ((3, 'Cate'), (4, 'Dex'))
}

db.executemany(**request)

```


### [Back to home](README.md)