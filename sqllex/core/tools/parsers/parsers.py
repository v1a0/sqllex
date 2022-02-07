from sqllex.types import *
from sqllex.constants import INNER_JOIN, LEFT_JOIN, CROSS_JOIN, LIKE
from sqllex.core.entities.abc.sql_column import AbstractColumn
from sqllex.core.entities.abc.sql_search_condition import SearchCondition


def from_as_(func: callable):
    """
    Decorator for catching AS argument from TABLE arg

    Parameters
    ----------
    func : callable
        SQLite3x method where_ args might contain AS

    Returns
    -------
    callable
        Decorated method with TABLE arg as string (instead list with AS)

    """

    def as_wrapper(*args, **kwargs):
        if isinstance(kwargs.get("TABLE"), (list, tuple)):
            TABLE = " ".join(t_arg for t_arg in kwargs.pop("TABLE"))
            kwargs.update({"TABLE": TABLE})

        return func(*args, **kwargs)

    return as_wrapper


def with_(func: callable) -> callable:
    """
    [Temporary disabled]Decorator for catching WITH argument in kwargs of method

    """

    def with_wrapper(*args, **kwargs):
        if "WITH" in kwargs:
            with_dict: WithType = kwargs.pop("WITH")
        else:
            with_dict: None = None

        return func(*args, **kwargs)

    return with_wrapper


def where_(placeholder: AnyStr = '?') -> callable:
    """
    Decorator for catching WHERE argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: where_statement.
    And adding values into :SQLStatement.values: if it has.

    Parameters
    ----------
    placeholder: str
        Symbol to use for placeholder

    Returns
    -------
    callable
        Decorated method with script contains where_statement and values contains values of where_statement
    """
    def where_pre_wrapper(func: callable):
        def where_wrapper(*args, **kwargs):
            if "WHERE" in kwargs:
                where_: WhereType = kwargs.pop("WHERE")
            else:
                where_: None = None

            __script, __values = func(*args, **kwargs)

            if where_:
                __script = f"{__script} WHERE ("

                if isinstance(where_, SearchCondition):
                    __script = f"{__script}{where_.script}"
                    __values += where_.values

                elif isinstance(where_, AbstractColumn):
                    __script = f"{__script}{where_}"

                elif isinstance(where_, dict):
                    for (key, values) in where_.items():
                        # parsing WHERE values

                        if not isinstance(values, list):
                            values = [values]

                        # Looking for equality or inequality
                        if len(values) > 1 and values[0] in [
                            "<", "<<", "<=",
                            ">=", ">>", ">",
                            "=", "==", "!=",
                            "<>", LIKE,
                        ]:
                            operator = values.pop(0)

                            if len(values) == 1 and isinstance(
                                    values[0], list
                            ):
                                values = values[0]
                        else:
                            operator = "="

                        __script += f"({f' {operator} {placeholder} OR '.join(str(key) for _ in values)} {operator} {placeholder} OR "   # spaaces need for [LIKE, regexp]
                        __script = f"{__script[:-3].strip()}) " + "AND "

                        if __values:
                            if isinstance(__values[0], tuple):
                                # if .values contains many values for insertmany __script, __values
                                # add where_ values for each value
                                new_values = list(__values)

                                for i in range(len(new_values)):
                                    new_values[i] = tuple(
                                        list(new_values[i]) + list(values)
                                    )

                                __values = tuple(new_values)

                            else:
                                # if .values contains only one set of values
                                # add where_ values
                                __values = tuple(
                                    list(__values) + list(values)
                                )
                        else:
                            __values = values

                    __script = __script.strip()[:-3]

                elif isinstance(where_, str):
                    __script += f"{where_}"

                else:
                    raise TypeError

                __script = (
                    f"{__script}) "  # .strip() removing spaces around
                )

            return __script, __values

        return where_wrapper

    return where_pre_wrapper


def join_(func: callable) -> callable:
    """
    Decorator for catching JOIN argument in kwargs of method

    If it has, adding into beginning of :SQLStatement.script: where_statement.
    And adding values into :SQLStatement.values: if it has.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg JOIN

    Returns
    ----------
    callable
        Decorated method with script contains join_statement and values contains values of join_statement

    """

    def join_wrapper(*args, **kwargs):
        def add_join_to_script(joins: tuple, base_script: str) -> str:
            if isinstance(joins, (list, tuple)):

                # if JOIN is not List[List] make it so
                if not isinstance(joins[0], (list, tuple)):
                    joins = (joins,)

                for _join in joins:
                    # If first element is JOIN type
                    if _join[0] in [INNER_JOIN, LEFT_JOIN, CROSS_JOIN]:
                        join_method = _join[0]
                        _join = _join[1:]
                    else:
                        join_method = INNER_JOIN

                    # Adding JOIN to script
                    base_script += f" {join_method} {' '.join(str(j_arg) for j_arg in _join)} "

            return base_script

        if "JOIN" in kwargs:
            JOIN: JoinArgType = kwargs.pop("JOIN")
        else:
            JOIN: None = None

        __script, __values = func(*args, **kwargs)

        if JOIN:
            if isinstance(JOIN, (list, tuple)):
                __script = add_join_to_script(joins=JOIN, base_script=__script)
            else:
                raise TypeError(f"Incorrect JOIN extension type, got {type(JOIN)}, expected list or tuple")

        return __script, __values

    return join_wrapper


def or_param_(func: callable) -> callable:
    """
    Decorator for catching OR argument in kwargs of method

    If it has, adding into beginning of :SQLStatement.script: or_statement.
    And adding values into :SQLStatement.values: if it has.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg JOIN

    Returns
    ----------
    callable
        Decorated method with script contains or_statement and values contains values of or_statement

    """

    def or_wrapper(*args, **kwargs):
        def add_or_arg_to_script(or_argument: str, base_script: str) -> str:
            return f"{base_script} OR {or_argument}"

        if "OR" in kwargs:
            or_arg: OrOptionsType = kwargs.pop("OR")
        else:
            or_arg: None = None

        if or_arg:
            kwargs.update(
                {
                    "script": add_or_arg_to_script(
                        or_argument=or_arg,
                        base_script=kwargs.get('script')
                    )
                }
            )

        return func(*args, **kwargs)

    return or_wrapper


def order_by_(func: callable) -> callable:
    """
    Decorator for catching ORDER_BY argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: order_by_statement.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg ORDER BY

    Returns
    ----------
    callable
        Decorated method with script contains order_by_statement and values contains values of order_by_statement
    """

    def order_by_wrapper(*args, **kwargs):

        if "ORDER_BY" in kwargs:
            order_by: OrderByType = kwargs.pop("ORDER_BY")
        else:
            order_by: None = None

        __script, __values = func(*args, **kwargs)

        if order_by:
            if isinstance(order_by, (str, int)):
                __script = f"{__script} ORDER BY {order_by} "
            elif isinstance(order_by, (list, tuple)):
                __script = f"{__script} ORDER BY "

                for i, ord_ob in enumerate(order_by):

                    __script = f"{__script}" \
                               f"{', ' if i!=0 and ord_ob.lower() not in ['asc', 'desc'] else ''}" \
                               f" " \
                               f"{ord_ob}"

                # __script = (
                #     f"{__script} ORDER BY {', '.join(str(item_ob) for item_ob in order_by)} "
                # )
            else:
                raise TypeError(f"Unexpected type of ORDER_BY parameter, "
                                f"expected str or tuple, got {type(order_by)} instead")

        return __script, __values

    return order_by_wrapper


def limit_(func: callable) -> callable:
    """
    Decorator for catching LIMIT argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: limit_statement.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg LIMIT

    Returns
    ----------
    callable
        Decorated method with script contains limit_statement and values contains values of limit_statement

    """

    def limit_wrapper(*args, **kwargs):
        if "LIMIT" in kwargs:
            limit: LimitOffsetType = kwargs.pop("LIMIT")
        else:
            limit: None = None

        __script, __values = func(*args, **kwargs)

        if limit:
            if isinstance(limit, (float, str)):
                limit = int(limit)
            __script = f"{__script} LIMIT {limit} "

        return __script, __values

    return limit_wrapper


def offset_(func: callable) -> callable:
    """
    Decorator for catching OFFSET argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: offset_statement.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg OFFSET

    Returns
    ----------
    callable
        Decorated method with script contains offset_statement and values contains values of offset_statement

    """

    def offset_wrapper(*args, **kwargs):
        if "OFFSET" in kwargs:
            offset: LimitOffsetType = kwargs.pop("OFFSET")
        else:
            offset: bool = False

        __script, __values = func(*args, **kwargs)

        if offset:
            if isinstance(offset, (float, str)):
                offset = int(offset)
            __script = f"{__script} OFFSET {offset} "

        return __script, __values

    return offset_wrapper


def group_by_(func: callable) -> callable:
    """
    Decorator for catching GROUP_BY argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: group_by_statement.

    Parameters
    ----------
    func : callable
        SQLite3x method contains kwarg GROUP_BY

    Returns
    ----------
    callable
        Decorated method with script contains group_by_statement

    """

    def group_by_wrapper(*args, **kwargs):
        if "GROUP_BY" in kwargs:
            group_by: GroupByType = kwargs.pop("GROUP_BY")
        else:
            group_by: None = None

        __script, __values = func(*args, **kwargs)

        if group_by:
            if not isinstance(group_by, (tuple, list)):
                group_by = (group_by,)

            __script = f"{__script} GROUP BY {', '.join(str(gr) for gr in group_by)} "

        return __script, __values

    return group_by_wrapper


__all__ = [
    'from_as_',
    'with_',
    'where_',
    'join_',
    'or_param_',
    'order_by_',
    'limit_',
    'offset_',
    'group_by_',
]
