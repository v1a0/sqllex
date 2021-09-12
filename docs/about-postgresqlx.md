# PostgreSQLx

Main class to interact with PostgreSQL databases, belongs to the sqllex-databases family, child of AbstractDatabase.

```python
# from sqllex import PostgreSQLx, INTEGER, TEXT, AUTOINCREMENT
from sqllex.classes import PostgreSQLx
from sqllex.constants.sqlite import INTEGER, TEXT, AUTOINCREMENT


db = PostgreSQLx(
    dbname="sqllextests",   # database name
    user="postgres",        # username
    password="admin",       # user's password
    host="127.0.0.1",       # psql host address 
    port="5432",            # connection port
    
    # Optional parameters
    template={
        'users': {
            'id': [INTEGER, AUTOINCREMENT],
            'name': TEXT
        }
    }
)

```

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
- [placeholder](database-properties.md#abstractdatabaseplaceholder)
- [port *](postgresqlx-properties.md#postgresqlxport)
- [tables](database-properties.md#abstractdatabasetables)
- [tables_names](database-properties.md#abstractdatabasetables_names)
- [user *](postgresqlx-properties.md#postgresqlxuser)


    * - available only for this specific database-class

### [Back to home](README.md)