# Engine

Engine is abstract class or module to isolate sqllex code from unnecessary dependencies.
Engine have to be corresponding to AbstractEngine class. 
You can find the current abstraction for engine in `sqllex/core/entities/abc/{engine.py | connection.py}`

## PostgreSQLx engine
Current abstraction for PostgreSQLx located in `sqllex/core/entities/postgresqlx/engine.py`

> Recommend to use psycopg2 (from the box)

```shell
pip install psycopg2
```

```python
import psycopg2
import sqllex as sx


db = sx.PostgreSQLx(
    engine=psycopg2,        # Postgres engine
    dbname="test_sqllex",   # database name
    user="postgres",        # username
    password="admin",       # user's password
    host="127.0.0.1",       # psql host address 
    port="5432",            # connection port
    
    # Optional parameters
    template={
        'users': {
            'id': [sx.INTEGER, sx.AUTOINCREMENT],
            'name': sx.TEXT
        }
    },
    
    # Create connection to database with database class object initialisation
    init_connection=True
)
```

Read more in [./about-postgresqlx.md](about-postgresqlx.md)