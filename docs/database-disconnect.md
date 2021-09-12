# AbstractDatabase.disconnect


```python
def disconnect(self):
    """
    Drop connection to database

    Commit changes and close connection

    """
```

Read more about connection in [sqlite3x-connect.md](sqlite3x-connect.md)
and [postgresqlx-connect.md](postgresqlx-connect.md)


## Examples

```python
from sqllex.classes import AbstractDatabase
from sqllex.constants import INTEGER

db: AbstractDatabase = ...

db.connect()

# ------------------ ANY INTERACTION WITH DATABASE -----------------------
db.create_table("numbers", {"value": [INTEGER]}, IF_NOT_EXIST=True)

for i in range(1000):
    db.insert("numbers", i, execute=False)
# ---------------------------- THE END  ----------------------------------

db.disconnect()

```

### [Back to home](README.md)