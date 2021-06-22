# SQLite3x.sqlect_all

```python
def select_all(
        self,
        TABLE: Union[str, List[str], SQLite3xTable] = None,
        SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
        WHERE: WhereType = None,
        WITH: WithType = None,
        ORDER_BY: OrderByType = None,
        LIMIT: LimitOffsetType = None,
        OFFSET: LimitOffsetType = None,
        FROM: Union[str, List[str], SQLite3xTable] = None,
        JOIN: Union[str, List[str], List[List[str]]] = None,
        **kwargs,
) -> Union[SQLStatement, List[Any]]:
    """
    SELECT all data from table

    Parameters
    ----------
    TABLE : AnyStr
        Name of table
    SELECT : Union[str, List[str]]
        columns to select. Value '*' by default
    WHERE : WhereType
        optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
    WITH : WithType
        with_statement (don't really work well)
    ORDER_BY : OrderByType
        optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
    LIMIT: LimitOffsetType
        optional parameter for conditions, example: 10
    OFFSET : LimitOffsetType
        optional parameter for conditions, example: 5
    FROM : str
        Name of table, same at TABLE
    JOIN: Union[str, List[str], List[List[str]]]
        optional parameter for joining data from other tables ['groups'],

    Returns
    ----------
    List[List]
        selected data

    """

```

Same as [SQLIte3x.select](./sqlite3x-select.md) 

### [Back to home](./index.md)
