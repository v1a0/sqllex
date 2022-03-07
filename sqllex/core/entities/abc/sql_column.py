"""
AbstractColumn
"""
from sqllex.types import AnyStr
from sqllex.constants import LIKE
from sqllex.core.entities.abc.sql_search_condition import SearchCondition


class AbstractColumn:
    """
    Sub-class of AbstractTable, itself it's one abstract column inside of abstract table
    Primary have the same methods but without table name argument

    This class existing for generating SearchConditions
    in constructions like this:
        db['table_name']['column_name'] = x
        db['table_name']['column_name'] > x
        db['table_name']['column_name'] >= x
        db['table_name']['column_name'] != x
        ...
        db['table_name']['column_name'] / x

        AND SPECIAL: column-like-reg_ex
        db['table_name']['column_name'] |LIKE| '%find_me%'
    """

    def __init__(self, table: str, name: AnyStr, placeholder='?'):
        """
        Attributes
        ----------
        table : AbstractTable
            Parent table object
        name : str
            Name of column
        placeholder : str
            Symbol used in scripts as placeholder

        """
        self.table = table
        self.name = name
        self.placeholder = placeholder

    def __str__(self) -> AnyStr:
        return f'"{self.table}"."{self.name}"'

    def _str_gen(self, value, operator: str) -> SearchCondition:
        if isinstance(value, SearchCondition):
            return SearchCondition(
                f"({self}{operator}({value.script})",
                values=(value.values,),
                placeholder=self.placeholder
            )
        elif isinstance(value, AbstractColumn):
            return SearchCondition(
                f"({self}{operator}{value})",
                placeholder=self.placeholder
            )
        else:
            return SearchCondition(
                f"({self}{operator}{self.placeholder})",
                values=(value,),
                placeholder=self.placeholder
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

    def __or__(self, value):
        """
        column-like-reg_ex
        column |LIKE| '%find_me%'
        """

        assert_msg = "Column object does not support '|' operator by itself. " \
                     "Supports only construction with LIKE (as syntax sugar): " \
                     "db['column'] |LIKE| '%find_me%' "

        assert value is LIKE, assert_msg    # lgtm [py/comparison-using-is]

        return SearchCondition(
                script=f"({self} LIKE {self.placeholder})",
                placeholder=self.placeholder,
                liked=True
            )

    def __hash__(self):
        return hash(f"'{self.name}'.'{self.table}'")

    # never used
    # def __list__(self) -> List[Any]:
    #     return self.table.select_all(self.name)
