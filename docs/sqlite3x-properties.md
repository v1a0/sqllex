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

### [Back to home](README.md)