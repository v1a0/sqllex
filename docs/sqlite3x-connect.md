# SQLite3x.connect

```python
def connect(
        self,
        path=None,
        **kwargs
) -> sqlite3.Connection:
    """
    Creating sqlite3.connect() connection to interact with database
    
    Optional parameters (default):
        path=self.path

    Additional kwargs for sqlite3.connect()
        path=None,
        timeout=None,
        detect_types=None,
        isolation_level=None,
        check_same_thread=None,
        factory=None,
        cached_statements=None,
        uri=None,
    """
```

Method to create connection with database, by default (if connection is not exist) temporary connection will
be automatically created with try to interact with the database and destroyed after. 

Without creating persistent connection interacting with database might be slower than with it. 
Highly recommend create connection manually.


## Examples

### Casual

```python
import sqllex as sx

db = sx.SQLite3x(path='db-1.db')
# db = sx.PostgreSQL(...)

db.connect()

# ------------------ ANY INTERACTION WITH DATABASE -----------------------
db.create_table("numbers", {"value": [sx.INTEGER]}, IF_NOT_EXIST=True)

for i in range(1000):
    db.insert("numbers", i, execute=False)
# ---------------------------- THE END  ----------------------------------
    
db.disconnect()
```
<!--
### Recommended

```python
import sqllex as sx

db = sx.SQLite3x(path='db-1.db')
# db = sx.PostgreSQL(...)

db = SQLite3x('db-1', init_connection=False)

with db.connect() as conn:
    db.create_table("numbers", {"value": [sx.INTEGER]}, IF_NOT_EXIST=True)

    for i in range(1000):
        db.insert("numbers", i, execute=False)

```
-->

### [Back to home](README.md)