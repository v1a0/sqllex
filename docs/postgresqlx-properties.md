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



### [Back to home](README.md)