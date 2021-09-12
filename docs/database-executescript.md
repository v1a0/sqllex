# AbstractDatabase.executescript

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


### [Back to home](README.md)