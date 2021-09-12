# AbstractDatabase.delete


```python
def delete(
        self,
        TABLE: str,
        WHERE: WhereType = None,
        WITH: WithType = None,
        **kwargs,
) -> None:
    """
    DELETE FROM table WHERE {something}
    
    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    WHERE : WhereType
       optional parameter for conditions
       > db: AbstractDatabase
       > ...
       > WHERE=(db['table_name']['column_name'] == 'some_value')
    WITH : WithType
        Disabled!
    """
```


## Examples

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER, NOT_NULL, TEXT

db: AbstractDatabase = ...

db.create_table(
    'users',
    {
        'id': [INTEGER],
        'name': [TEXT, NOT_NULL]
    }
)


id_column = db['users']['id']


db.delete('users', id_column == 2)

db.delete(
    TABLE='users',
    WHERE=(
        id_column == 3
    )
)

db.delete(
    TABLE='users',
    WHERE=(
        id_column < 4
    )
)

db.delete(
    TABLE='users',
    WHERE=(
        (id_column != 5) & (id_column != 6) & (id_column != 7)
    )
)

```


### [Back to home](README.md)