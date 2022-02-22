# AbstractDatabase.add_column

```python
@property
def transaction(self) -> AbstractTransaction:
    """
    Property to create transaction statement. Have to be used inside 'with' statement.
    """
    ...

class AbstractTransaction(ABC):
    """
    Class for creating transactions. Have to be used inside 'with' statement

        .commit() - commit current transaction
        .rollback() - rollback current transaction
        .begin() - begin new transaction (experimental)

    """
    ...
```

# Examples

```python
import sqllex as sx

db = sx.SQLite3x('some.db')

with db.transaction as tran:
   try:
       # Transaction body
       # db.execute(...)
       ...
       tran.commit() # optional
        
   except Exception:
       tran.rollback()  # rollback transaction is something goes wrong
   

# the end
```


```python
import sqllex as sx
import sqlite3

db = sx.SQLite3x('some.db')
db.create_table(
    name='user',
    columns={
        'id': [sx.INTEGER, sx.PRIMARY_KEY],
        'name': [sx.TEXT]
    }
)


with db.transaction as tran:
    try:
        db['user'].insert(1, 'Alex')
        tran.commit()   # optional
    
    except sqlite3.IntegrityError:
        print("Transaction rolled back!")
        tran.rollback()

        
with db.transaction as tran:
    try:
        db['user'].insert(1, 'Flex')
    
    except sqlite3.IntegrityError:
        print("Transaction rolled back!")
        tran.rollback()
```


### [Back to home](README.md)