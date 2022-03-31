# PostgreSQLx

Main class to interact with PostgreSQL databases, belongs to the sqllex-databases family, child of AbstractDatabase.
Postgres database need `engine`, we recommend to use psycopg2, just import this lib and give it to Database class constructor.
You can read more [about engines here](./about-engines.md).

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

PostgreSQL now is only partially support. 
It has the same api interface as SQLite3x so feel free to use documentation
of it for PostgreSQLx. Just replace `SQLite3x` at `PostgreSQLx`.


## PostgreSQLx Public Methods 

- [add_column](database-add_column.md)
- [connect](postgresqlx-connect.md)
- [create_table](database-create_table.md)
- [create_temp_table](database-create_table.md)
- [create_temporary_table](database-create_table.md)
- [delete](database-delete.md)
- [disconnect](database-disconnect.md)
- [drop](database-drop.md)
- [execute](database-execute.md)
- [executemany](database-executemany.md)
- [executescript](database-executescript.md)
- [get_columns](database-get_columns.md)
- [get_columns_names](database-get_columns_names.md)
- [get_table](database-get_table.md)
- [insert](database-insert.md)
- [insertmany](database-insertmany.md)
- [markup](database-markup.md)
- [remove_column](database-remove_column.md)
- [~~replace~~]()
- [select](database-select.md)
- [select_all](database-select_all.md)
- [~~select_distinct~~]()
- [~~table_info~~]()
- [update](database-update.md)
- [updatemany](database-updatemany.md)


## Properties

- [connection](postgresqlx-properties.md#postgresqlxconnection)
- [dbname *](postgresqlx-properties.md#postgresqlxdbname)
- [host *](postgresqlx-properties.md#postgresqlxhost)
- [placeholder](postgresqlx-properties.md#postgresqlxplaceholder)
- [port *](postgresqlx-properties.md#postgresqlxport)
- [tables](postgresqlx-properties.md#postgresqlxtables)
- [tables_names](postgresqlx-properties.md#postgresqlxtables_names)
- [user *](postgresqlx-properties.md#postgresqlxuser)


```
    * - available only for this specific database-class
```

### [Back to home](README.md)