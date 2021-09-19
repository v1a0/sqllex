# SQLite3x

Main class to interact with SQLite3 databases, belongs to the sqllex-databases family, child of AbstractDatabase.

```python
# from sqllex import SQLite3x, INTEGER, TEXT, AUTOINCREMENT
from sqllex.classes import SQLite3x
from sqllex.constants.sqlite import INTEGER, TEXT, AUTOINCREMENT

db = SQLite3x(
    path="data/my_data.db", # path to db location, might be Path type
    
    # Optional parameters
    template={
        'users': {
            'id': [INTEGER, AUTOINCREMENT],
            'name': TEXT
        }
    }
)

```

## SQLite3x Public Methods

- [add_column](database-add_column.md)
- [connect](sqlite3x-connect.md)
- [create_table](database-create_table.md)
- [create_temp_table](database-create_table.md)
- [create_temporary_table](database-create_table.md)
- [delete](database-delete.md)
- [disconnect](database-disconnect.md)
- [drop](database-drop.md)
- [execute](database-execute.md)
- [executemany](database-executemany.md)
- [executescript](database-executescript.md)
- [foreign_keys *](sqlite3x-pragma.md#sqlite3xforeign_keys)
- [get_columns](database-get_columns.md)
- [get_columns_names](database-get_columns_names.md)
- [get_table](database-get_table.md)
- [insert](database-insert.md)
- [insertmany](database-insertmany.md)
- [journal_mode *](sqlite3x-pragma.md)
- [markup](database-markup.md)
- [pragma *](sqlite3x-pragma.md#sqlite3xpragma)
- [remove_column](database-remove_column.md)
- [replace *](sqlite3x-replace.md)
- [select](database-select.md)
- [select_all](database-select_all.md)
- [~~select_distinct~~](database-select.md)
- [table_info *](sqlite3x-pragma.md#sqlite3xtable_info)
- [update](database-update.md)
- [updatemany](database-updatemany.md)


## Properties

- [path *](sqlite3x-properties.md#sqlite3xpath)
- [connection](sqlite3x-properties.md#sqlite3xconnection)
- [placeholder](database-properties.md#abstractdatabaseplaceholder)
- [tables](database-properties.md#abstractdatabasetables)
- [tables_names](database-properties.md#abstractdatabasetables_names)


```
    * - available only for this specific database-class
```

### [Back to home](README.md)