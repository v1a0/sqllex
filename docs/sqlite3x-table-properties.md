# SQLite3xTable properties and constants


## SQLite3xTable.db

```python
db: SQLite3xTable
```

Parent database, where this table exist



## SQLite3xTable.name

```python
name: AnyStr
```

Name fo table as strings



## SQLite3xTable.columns

```python
@property
def columns(self) -> Generator[AbstractTable, None, None]:
    for column in self.columns_names:
        yield AbstractColumn(table=self, name=column)
```

Generator of columns as AbstractColumn objects



## SQLite3xTable.columns_names

```python
@property
def columns_names(self) -> List:
    return self.get_columns_names()
```

List of columns names as strings



### [Back to home](README.md)