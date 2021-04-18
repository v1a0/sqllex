<div align="center">

# SQLite3x.pragma

</div><br>

## About

Method to Set PRAGMA params

```python
def pragma(self,
           *args: str,
           **kwargs
           ) -> Union[List, None]:
```
> :param args: Pragma args

> :param kwargs: Pragma kwargs


## Child methods

### SQlite3x.foreign_keys

Turn on/off PRAGMA param FOREIGN KEYS

>:param mode: "ON" or "OFF"

```python
def foreign_keys(self,
                 mode: Literal["ON", "OFF"]
                 )
```


### SQlite3x.journal_mode

Set PRAGMA param journal_mode

> :param mode: "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"

```python
def journal_mode(self,
                 mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
                 )
```


### SQlite3x.table_info

Send PRAGMA request table_info(table_name)

>:param table_name: Name of table

```python
def table_info(self,
               table_name: str
               )
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





Read also:
- SQLite3x.drop