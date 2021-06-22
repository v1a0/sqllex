<div align="center">

# SQLite3x.pragma

</div><br>

## About

Method to set PRAGMA parameter or send PRAGMA-request

```python
def pragma(
        self,
        *args: str,
        **kwargs: NumStr
) -> Union[List, None]:
    """
    Set PRAGMA parameter or send PRAGMA-request
    Parameters
    ----------
    args : str
        Might be used like this:
        Example: db.pragma("database_list")
    kwargs : NumStr
        Might be used like this:
        Example: db.pragma(foreign_keys="ON")
    Returns
    ----------
    Union[List, None]
        Database answer if it has
    """
```

## Child methods

### SQlite3x.foreign_keys

Turn on/off PRAGMA param FOREIGN KEYS

>:param mode: "ON" or "OFF"

```python
def foreign_keys(
        self,
        mode: Literal["ON", "OFF"]
):
    """
    Turn on/off PRAGMA parameter FOREIGN KEYS
    Parameters
    ----------
    mode : Literal["ON", "OFF"]
        "ON" or "OFF" FOREIGN KEYS support
    """
```


### SQlite3x.journal_mode

Set PRAGMA param journal_mode

> :param mode: "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"

```python
def journal_mode(
        self,
        mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
):
    """
    Set PRAGMA param journal_mode
    Parameters
    ----------
    mode : Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
        Journal mode
    """
```


### SQlite3x.table_info

Send PRAGMA request table_info(table_name)

>:param table_name: Name of table

```python
def table_info(
        self,
        table_name: str
):
    """
    Send table_info PRAGMA request
    Parameters
    ----------
    table_name : str
        Name of table
    """
```


## Examples

```python

from sqllex import *

db = SQLite3x(path='database.db')

db.pragma("database_list")

db.pragma(foreign_keys="ON")

db.foreign_keys("OFF")

db.journal_mode("WAL")

db.table_info('my_table')

```

### [Back to home](./index.md)