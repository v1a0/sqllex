# SQLite3x.executescript

```python
def executescript(
        self,
        script: AnyStr = None,
        request: SQLRequest = None
) -> Union[List, None]:
    """
    Execute many SQL-scripts whit (or without) values
    Parameters
    ----------
    script : AnyStr
        single SQLite script, might contains placeholders
    request : SQLRequest
        Instead of script and values might execute full statement
    Returns
    ----------
    Union[List, None]
        Database answer if it has
    """
```

Sames as sqlite3.executescript


### [Back to home](README.md)