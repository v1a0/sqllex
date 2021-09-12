# AbstractDatabase.execute

```python
def execute(
        self,
        script: AnyStr = None,
        values: Tuple = None,
) -> Union[Tuple, None]:
    """
    Execute any SQL-script whit (or without) values
    
    Parameters
    ----------
    script : AnyStr
        single SQLite script, might contains ph_amount
    values : Tuple
        Values for ph_amount if script contains it
    
    Returns
    ----------
    Union[Tuple, None]
        ABDatabase answer if it has
    """
```


## Examples

```python
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

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