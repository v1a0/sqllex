# PostgreSQLx properties

## PostgreSQLx.connection

```python
@property
def connection(self) -> Union[connection, None]:
    return self.__connection
```

Connection object `psycopg2.extensions.connection` to database, if has, else `None`.


## PostgreSQLx.dbname

```python
@property
def dbname(self) -> AnyStr:
    return self.__dbname
```

Name of database to connect, `"postgres"` by default.


## PostgreSQLx.host

```python
@property
def host(self) -> AnyStr:
    return self.__host
```

Host address of postgres server, localhost by default.


## PostgreSQLx.port

```python
@property
def port(self) -> AnyStr:
    return self.__port
```

Port of postgres server, 5432 by default


## PostgreSQLx.user

```python
@property
def user(self) -> AnyStr:
    return self.__user
```

Username to login, "postgres" by default.

---


## PostgreSQLx.tables

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

## PostgreSQLx.tables_names

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


## PostgreSQLx.placeholder

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


## PostgreSQLx.transaction

Read more in [./database-transaction.md](./database-transaction.md)

### [Back to home](README.md)