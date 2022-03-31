# SQLite3x.disconnect


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
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

db.connect()

# ------------------ ANY INTERACTION WITH DATABASE -----------------------
db.create_table(
    "numbers", 
    {
        "value": [sx.INTEGER]
    }, 
    IF_NOT_EXIST=True
)

for i in range(1000):
    db["numbers"].insert(i)
# ---------------------------- THE END  ----------------------------------

db.disconnect()

```

### [Back to home](README.md)