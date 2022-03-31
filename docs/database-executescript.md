# SQLite3x.executescript

```python
def executescript(
        self,
        script: AnyStr = None,
) -> Union[Tuple, None]:
    """
    Execute many SQL-scripts whit (or without) values
    
    Parameters
    ----------
    script : AnyStr
        single SQLite script, might contains ph_amount
        
    Returns
    ----------
    Union[Tuple, None]
        ABDatabase answer if it has
    """
```

Sames as sqlite3.executescript


## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.executescript(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY UNIQUE,
        name TEXT
    );
    INSERT INTO users (id, text) VALUES (1, 2);
    INSERT INTO users (id, text) VALUES (2, 3);
    """
)
```

### [Back to home](README.md)