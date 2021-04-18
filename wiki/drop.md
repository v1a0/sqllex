<div align="center">

# SQLite3x.drop

</div><br>

## About

Method to DROP TABLE (IF EXIST)

```python
def drop(self,
         TABLE: AnyStr,
         IF_EXIST: bool = True,
         execute: bool = True,
         **kwargs
         ):
```


> :param TABLE: Table name as string

> :param IF_EXIST: Check is table exist (boolean)

>:param execute: Execute script and return db's answer (True) or return script (False)



## Examples

```python

from sqllex import *

db = SQLite3x(
    path='database.db',
    template={
        'table1': {'id': INTEGER},
        'table2': {'id': INTEGER},
        'table3': {'id': INTEGER},
    }
)

db.drop('table1')
db.drop(TABLE='table2')
db.drop(TABLE='table3', IF_EXIST=True)

```

Read also:
- SQLite3x.create_table