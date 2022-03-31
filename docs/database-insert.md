# SQLite3x.insert


```python
def insert(
        self,
        TABLE: Union[AnyStr, AbstractTable],
        *args: InsertingData,
        OR: OrOptionsType = None,
        WITH: WithType = None,
        **kwargs: Any,
) -> None:
    """
    INSERT data into table
    
    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    OR : OrOptionsType
        Action in case if inserting has failed. Optional parameter.
        > OR='IGNORE'
    WITH : WithType
        Disabled!
    """
```

## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER],
        'name': [sx.TEXT, sx.NOT_NULL]
    }
)

db.insert('user', 1, 'User1')

db.insert('user', [2, "User2"])

db.insert('user', (3, 'User3'))

db.insert('user', id=4, name="User4")

db.insert(
    TABLE='user',
    id=5, name="User5"
)

db.insert('user', name="User6")

db.insert(
    'users',
    [100, 'Dex1'],
    OR=sx.IGNORE  # REPLACE, FAIL, ABORT, ROLLBACK
)

db.insert(
    'users',
    [200, 'Dex2'],
    OR=sx.REPLACE 
)

db.insert(
    'users',
    [300, 'Dex3'],
    OR=sx.ABORT
)

```


### [Back to home](README.md)