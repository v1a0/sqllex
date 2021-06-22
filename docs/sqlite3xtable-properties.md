# SQLite3xTable properties and constants


## SQLite3xTable.db

```python
SQLite3xTables.db: SQLite3x
```

Parent database, where this table exist



## SQLite3xTable.name

```python
SQLite3xTables.name: AnyStr
```

Name fo table as strings



## SQLite3xTable.columns

```python
@property
def columns(self) -> Generator[SQLite3xColumn, None, None]:
    for column in self.columns_names:
        yield SQLite3xColumn(table=self, name=column)
```

Generator of columns as SQLite3xColumn objects



## SQLite3xTable.columns_names

```python
@property
def columns_names(self) -> List:
    return self.get_columns_names()
```

List of columns names as strings



### [Back to home](./index.md)