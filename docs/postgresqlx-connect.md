# PostgreSQLx.connect

```python
@copy_docs(ABDatabase.connect)
def connect(self, password: AnyStr):
    """
    Creating psycopg2.extensions.connection to interact with database
    """
```

Method to create connection with database, by default (if connection is not exist)
temporary connection will be automatically created with try to interact with the 
database and destroyed after. 

Without creating persistent connection interacting with database might be slower than with it. 
Highly recommend create connection manually.


## Examples

```python
import sqllex

db = sqllex.PostgreSQLx('db-1')

db.connect()

# ------------------ ANY INTERACTION WITH DATABASE -----------------------
db.create_table("numbers", {"value": [sqllex.INTEGER]}, IF_NOT_EXIST=True)

for i in range(1000):
    db.insert("numbers", i, execute=False)
# ---------------------------- THE END  ----------------------------------
    
db.disconnect()

```

### [Back to home](README.md)