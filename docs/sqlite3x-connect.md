# SQLite3x.connect

```python
def connect(self):
    """
    Create connection to database
    Creating sqlite3.connect(__str__) connection to interact with database
    """
```

Method to create connection with database, by default (if connection is not exist) temporary connection will be automatically created with try to interact with the database and destroyed after. Without creating persistent connection interacting with database might be slower than with it. Highly recommend to use all the time.

For example, inserting 1000 values by SQLite3x.insert() method:

    sqllex_connect  0.0529s
    sqllex_without_connect  6.35s
    sqlite3  0.0156s


## Examples

```python
import sqllex

db = sqllex.SQLite3x('db-1')

db.connect()

# ------------------ ANY INTERACTION WITH DATABASE -----------------------
db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)

for i in range(1000):
    db.insert("numbers", i, execute=False)
# ---------------------------- THE END  ----------------------------------
    
db.disconnect()

```

### [Back to home](README.md)