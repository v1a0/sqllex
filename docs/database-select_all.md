# AbstractDatabase.select_all

```python
def select_all(
        self,
        TABLE: Union[AnyStr, AbstractTable] = None,
        SELECT: Union[str, AbstractColumn, ConstantType, List, Tuple] = None,
        WHERE: WhereType = None,
        WITH: WithType = None,
        ORDER_BY: OrderByType = None,
        LIMIT: LimitOffsetType = None,
        OFFSET: LimitOffsetType = None,
        FROM: Union[str, List[str], AbstractTable] = None,
        JOIN: JoinArgType = None,
        **kwargs,
) -> List[Tuple]:
    """
    SELECT all data from table
    
    Parameters
    ----------
    TABLE : Union[str, AbstractTable]
        Name of table
    SELECT : Union[str, AbstractColumn, List, Tuple]
        columns to select. Value '*' by default
     WHERE : WhereType
        optional parameter for conditions
        > WHERE=(db['table_name']['column_name'] == 'some_value')
    WITH : WithType
        Disabled!
    ORDER_BY : OrderByType
        optional parameter for conditions
        > ORDER_BY=['age', 'DESC']
        > ORDER_BY='age DESC'
    ORDER_BY : OrderByType
        optional parameter for conditions
        > ORDER_BY=['age', 'DESC']
        > ORDER_BY='age DESC'
    LIMIT: LimitOffsetType
        Set limit or selecting records
        > LIMIT=10
    OFFSET : LimitOffsetType
        Set offset for selecting records
        > OFFSET=5
    JOIN: Union[str, List[str], List[List[str]]]
        optional parameter for joining data from other tables ['groups'],
    FROM : Union[str, List[str], AbstractTable]
        Name of table, same at TABLE
    
    Returns
    ----------
    Tuple[Tuple]
        Selected data
    """
```

Same as [SQLIte3x.select](database-select.md) but SELECT parameter == ALL

### [Back to home](README.md)
