"""
SearchCondition
"""
from sqllex.types import AnyStr


class SearchCondition:
    def __init__(self, script: AnyStr, values=tuple(), placeholder='?', liked=False):
        self.script = script
        self.values = values
        self.placeholder = placeholder
        self.liked = liked

    def __str__(self):
        return self.script

    def _str_gen(self, value, operator: str):
        assert not self.liked,  "Column-LIKE-reg_ex' structure doesn't have second part. " \
                                "Expected: 'column |LIKE| reg_ex'. " \
                                f"Got 'column |LIKE{operator} value' instead."


        if isinstance(value, SearchCondition):
            return SearchCondition(
                f"({self}{operator}{value.script})",
                values=self.values + value.values
            )

        else:
            return SearchCondition(
                f"({self}{operator}{self.placeholder})",
                values=self.values + (value,)
            )

    def __lt__(self, value):
        return self._str_gen(value, '<')

    def __le__(self, value):
        return self._str_gen(value, '<=')

    def __eq__(self, value):
        return self._str_gen(value, '=')

    def __ne__(self, value):
        return self._str_gen(value, '<>')

    def __gt__(self, value):
        return self._str_gen(value, '>')

    def __ge__(self, value):
        return self._str_gen(value, '>=')

    def __and__(self, other):
        return self._str_gen(other, ' AND ')

    def __or__(self, value):
        if self.liked:
            self.values += (value,)
            return self
        else:
            return self._str_gen(value, ' OR ')

    def __hash__(self):
        return hash(f"{self.script}")
