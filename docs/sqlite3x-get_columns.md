# SQLite3x.get_columns

```python
def get_columns(
        self,
        table: AnyStr
) -> Generator[SQLite3xColumn, None, None]:
    """
    Get list of table columns like an SQLite3xColumn objects
    Parameters
    ----------
    table : AnyStr
        Name of table
    Returns
    ----------
    Generator[SQLite3xColumn]
        Columns of table
    """
```

### [Back to home](./index.md)