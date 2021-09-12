# AbstractTable properties and constants


## AbstractTable.db

```python
db: AbstractDatabase
```

Parent database, where this table exist



## AbstractTable.name

```python
name: AnyStr
```

Name fo table as strings



## AbstractTable.columns

```python
@property
def columns(self) -> Generator[AbstractTable, None, None]:
    for column in self.columns_names:
        yield AbstractColumn(table=self, name=column)
```

Generator of columns as AbstractColumn objects



## AbstractTable.columns_names

```python
@property
def columns_names(self) -> List:
    return self.get_columns_names()
```

List of columns names as strings



### [Back to home](README.md)