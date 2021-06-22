# SQLite3x properties and constants


## SQLite3x.path

```python
@property
    def path(self) -> PathType:
        return self.__path
```

Path to database, `Str` or `PathType`



## SQLite3x.connection

```python
@property
def connection(self) -> Union[sqlite3.Connection, None]:
    return self.__connection
```

Connection object `sqlite3.Connection` to database, if have no == None 



## SQLite3x.tables

```python
@property
def tables(self) -> Generator[SQLite3xTable, None, None]:
    return self._get_tables()
```

Generator of tables as SQLite3xTable objects 



## SQLite3x.tables_names

```python
@property
def tables_names(self) -> List[str]:
    return self._get_tables_names()
```

List of tables names as strings


### [Back to home](./index.md)