# SQLite3x.updatemany

```python
def updatemany(
        self,
        TABLE: Union[AnyStr, AbstractTable],
        SET: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple]] = None,
        **kwargs,
) -> None:
    """
    ACTUALLY IT'S JUST "INSERT OR REPLACE" BUT SOUNDS EASIER TO UNDERSTAND
    Update (or insert) many values
    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    SET : Union[List, Tuple, Mapping]
        Values to insert or update
        P.S: SET also support numpy.array value
    """
```


# Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    't6',
    {
        'id': sx.INTEGER,
        'val': sx.TEXT
    },
    IF_NOT_EXIST=True
)

data1 = [[x, 'hi'] for x in range(100_000)]
data2 = [[x, 'bye'] for x in range(100_000)]


db.insertmany('t6', data1)

# HERE !! vvvvvvvvvvvvvvvv

db.updatemany('t6', data2)

db.insertmany('t6', data2, OR=sx.REPLACE)  # actually do the same thing

```


### [Back to home](README.md)