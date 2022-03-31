# SQLite3x properties


## SQLite3x.path

```python
@property
def path(self) -> PathType:
    return self.__path
```

Path to database, `Str` or `PathType`

---

## SQLite3x.connection

```python
@property
def connection(self) -> Union[sqlite3.Connection, None]:
    return self.__connection
```

Connection object `sqlite3.Connection` to database, if has, else `None`

---

## SQLite3x.tables

```python
@property
def tables(self) -> Generator[AbstractDatabase, None, None]:
    return self._get_tables()
```

Generator of tables-objects (existing in a database)

```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

print(db.table)  # <Generator object at 0x1337>

for table in db.tables:
    print(table.name)   # 'table_1'      # 'table_2'      # 'table_3'
```

---

## SQLite3x.tables_names

```python
@property
def tables_names(self) -> List[str]:
    return self._get_tables_names()
```

List of tables names (existing in a database) as strings


```python
import sqllex as sx

db = sx.SQLite3x(path='database.db')
# db = sx.PostgreSQL(...)

print(db.tables_names)  # ('table_1', 'table_2', 'table_3')
```


---


## SQLite3x.placeholder

```python
@property
def placeholder(self) -> str:
    return self.__placeholder
```

Just placeholder symbol, '?' for sqlite and '%s' for postgresql and so on.

```python
import sqllex as sx

postgres_db: sx.PostgreSQLx = ...
sqlite_db: sx.SQLite3x = ...

print(postgres_db.placeholder) # %s
print(sqlite_db.placeholder)   # ?
```


## SQLite3x.transaction

Read more in [./database-transaction.md](./database-transaction.md)

### [Back to home](README.md)