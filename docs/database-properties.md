# Common properties for database-classes

## AbstractDatabase.tables

```python
@property
def tables(self) -> Generator[AbstractDatabase, None, None]:
    return self._get_tables()
```

Generator of tables-objects (existing in a database)

```python
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

print(db.table)  # <Generator object at 0x1337>

for table in db.tables:
    print(table.name)   # 'table_1'      # 'table_2'      # 'table_3'
```

---

## AbstractDatabase.tables_names

```python
@property
def tables_names(self) -> List[str]:
    return self._get_tables_names()
```

List of tables names (existing in a database) as strings


```python
from sqllex.classes import AbstractDatabase

db: AbstractDatabase = ...

print(db.tables_names)  # ('table_1', 'table_2', 'table_3')
```



## AbstractDatabase.placeholder

```python
@property
def placeholder(self) -> str:
    return self.__placeholder
```

Just placeholder symbol, '?' for sqlite and '%s' for postgresql and so on.

```python
from sqllex.classes import SQLite3x, PostgreSQLx

postgres_db: PostgreSQLx = ...
sqlite_db: SQLite3x = ...

print(postgres_db.placeholder) # %s
print(sqlite_db.placeholder)   # ?
```