# SQLite3x.replace

```python
def replace(
        self,
        TABLE: Union[AnyStr, AbstractTable],
        *args: Any,
        WHERE: WhereType = None,
        **kwargs: Any,
) -> None:
    """
    REPLACE data into table
    
    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    WHERE : WhereType
        Optional parameter for conditions
        > WHERE=(db['table_name']['column_name'] == 'some_value')
    
    """
```

## Examples

```python
import sqllex as sx

db = sx.SQLite3x(path='db-1.db')
# db = sx.PostgreSQL(...)

db.create_table(
    'users',
    {
        'id': [sx.INTEGER, sx.PRIMARY_KEY, sx.UNIQUE],
        'name': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, 'Unknown']
    }
)

...

db.replace('users', 1, 'User1')

db.replace('users', [2, "User2"])

db.replace('users', (3, 'User3'))

db.replace('users', id=4, name="User4")

db.replace(
    TABLE='users',
    id=5, name="User5"
)

# for SQLIte3xTable

users = db['users']

users.replace([5, "User5"])

```


### [Back to home](README.md)