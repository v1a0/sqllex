# SQLite3x.pragma

```python
def pragma(
        self,
        *args: str,
        **kwargs: NumStr
) -> Union[Tuple, None]:
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
    Union[Tuple, None]
        ABDatabase answer if it has
    """
```

## Child methods

### SQLite3x.foreign_keys

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

#### Example

```python
db: SQLite3x
db.foreign_keys('ON')
db.foreign_keys('OFF')
```


### SQLite3x.journal_mode

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

#### Example

```python
db: SQLite3x
db.journal_mode('DELETE')
db.journal_mode('WAL')
```


### SQLite3x.table_info

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

#### Example

```python
db: SQLite3x

print(
    db.table_info('table_name')
)
print(
    db['table_name'].info('WAL')
)
```


## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')

db.pragma("database_list")

db.pragma(foreign_keys="ON")

db.foreign_keys("OFF")

db.journal_mode("WAL")

db.table_info('my_table')

```

### [Back to home](README.md)