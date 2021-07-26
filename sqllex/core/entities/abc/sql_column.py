from sqllex.types import AnyStr
from sqllex.core.entities.abc.sql_search_condition import SearchCondition


class AbstractColumn:
    """
    Sub-class of AbstractTable, itself one column of table (AbstractTable)
    Have same methods but without table name argument
    Attributes
    ----------
    table : AbstractTable
        AbstractTable parent table object
    name : str
        Name of column

    Existing for generating SearchCondition for WHERE, SET
    and other parameters of parents classes

    db['table_name']['column_name'] = x
    db['table_name']['column_name'] > x
    db['table_name']['column_name'] >= x
    db['table_name']['column_name'] != x
    ...
    db['table_name']['column_name'] / x
    """

    def __init__(self, table: str, name: AnyStr):
        self.table = table
        self.name = name

    def __str__(self):
        return f"'{self.table}'.'{self.name}'"

    def _str_gen(self, value, operator: str):
        if isinstance(value, SearchCondition):
            return SearchCondition(
                f"({self}{operator}({value.script})",
                values=(value.values,)
            )
        elif isinstance(value, AbstractColumn):
            return SearchCondition(
                f"({self}{operator}{value}",
            )
        else:
            return SearchCondition(
                f"({self}{operator}?)",
                values=(value,)
            )

    def __lt__(self, value) -> SearchCondition:
        return self._str_gen(value, '<')

    def __le__(self, value) -> SearchCondition:
        return self._str_gen(value, '<=')

    def __eq__(self, value) -> SearchCondition:
        return self._str_gen(value, '=')

    def __ne__(self, value) -> SearchCondition:
        return self._str_gen(value, '<>')

    def __gt__(self, value) -> SearchCondition:
        return self._str_gen(value, '>')

    def __ge__(self, value) -> SearchCondition:
        return self._str_gen(value, '>=')

    def __add__(self, value) -> SearchCondition:
        return self._str_gen(value, '+')

    def __sub__(self, value) -> SearchCondition:
        return self._str_gen(value, '-')

    def __mul__(self, value) -> SearchCondition:
        return self._str_gen(value, '*')

    def __truediv__(self, value) -> SearchCondition:
        return self._str_gen(value, '/')

    def __divmod__(self, value) -> SearchCondition:
        return self._str_gen(value, '%')

    # def __list__(self) -> List[Any]:
    #     return self.table.select_all(self.name)

    def __hash__(self):
        return hash(f"'{self.name}'.'{self.table}'")

