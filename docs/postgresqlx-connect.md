# PostgreSQLx.connect

```python
def connect(
        self,
        password: AnyStr,
        dbname=None,
        user=None,
        host=None,
        port=None,
        **kwargs
):
    """
    Creating psycopg2.extensions.connection to interact with database
    
    Optional parameters (default):
        dbname=self.dbname,
        user=self.user,
        host=self.host,
        port=self.port,

    Additional kwargs for psycopg2.connect()
        dsn=None,
        connection_factory=None,
        cursor_factory=None,

    """
```

Method to create connection with database, by default (if connection is not exist)
temporary connection will be automatically created with try to interact with the 
database and destroyed after. 

Without creating persistent connection interacting with database might be slower than with it. 
Highly recommend create connection manually.


## Examples

### Casual

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