from sqllex.types import *
from sqllex.constants.sql import *
import cProfile
import pstats


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
        if "TABLE" in kwargs.keys():

            if isinstance(kwargs.get("TABLE"), list) and AS in kwargs.values():
                TABLE = " ".join(t_arg for t_arg in kwargs.pop("TABLE"))
                kwargs.update({"TABLE": TABLE})

        return func(*args, **kwargs)

    return as_wrapper


def with_(func: callable) -> callable:
    """
    Decorator for catching WITH argument in kwargs of method

    If it has, adding into beginning of :SQLStatement.script: with_statement.
    And adding values into :values: if it has.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg WITH

    Returns
    -------
    callable
        Decorated method with script contains with_statement and values contains values of with_statement

    Raise
    -------
    TypeError
        If value of WHERE dict is not SQLStatement or str
    """

    def with_wrapper(*args, **kwargs):
        if "WITH" in kwargs.keys():
            with_dict: WithType = kwargs.pop("WITH")
        else:
            with_dict: None = None

        # if with_dict:
        #     script = f"WITH RECURSIVE "
        #     values = []
        #
        #     for (var, statement) in with_dict.items():
        #
        #         # Checking is value of dict SQLStatement or str
        #         if issubclass(type(statement), SQLStatement):
        #             condition = statement.request
        #             script += f"{var} AS ({condition.script.strip()}), "  # .strip() removing spaces around
        #             values += list(condition.values)
        #
        #         elif isinstance(statement, str):
        #             condition = statement
        #             script += f"{var} AS ({condition}), "
        #
        #         else:
        #             raise TypeError(f"Unexpected type of WITH value\n"
        #                             f"Got {type(statement)} instead of SQLStatement or str")
        #
        #     if script[-2:] == ', ':
        #         script = script[:-2]
        #
        #     kwargs.update(
        #         {
        #             "values": tuple(values)
        #             if not kwargs.get("values")
        #             else tuple(list(kwargs.get("values")) + list(values)),
        #
        #             "script": f"{script} "
        #             if not kwargs.get("script")
        #             else f"{script} " + kwargs.get("script"),
        #         }
        #     )

        return func(*args, **kwargs)

    return with_wrapper


def where_(func: callable) -> callable:
    """
    Decorator for catching WHERE argument in kwargs of method

    If it has, adding in the end of :SQLStatement.script: where_statement.
    And adding values into :SQLStatement.values: if it has.

    Parameters
    ----------
    func : callable
        SQLite3x method contains arg WHERE

    Returns
    -------
    callable
        Decorated method with script contains where_statement and values contains values of where_statement
    """

    def where_wrapper(*args, **kwargs):
        if "WHERE" in kwargs.keys():
            where_: WhereType = kwargs.pop("WHERE")

        else:
            where_: None = None

        stmt: SQLStatement = func(*args, **kwargs)

        if where_:
            stmt.request.script += f"WHERE ("

            if isinstance(where_, tuple):  #
                where_ = list(where_)

            if isinstance(where_, list):

                # If WHERE is not List[List] (Just List[NotList])
                if not isinstance(where_[0], list):
                    where_ = [where_]

                new_where = {}

                for wh in where_:

                    # List[List] -> Dict[val[0], val[1]]

                    if isinstance(wh[0], str) and len(wh) > 1:
                        new_where.update({wh[0]: wh[1:]})
                    else:
                        raise TypeError(f"Unexpected type of WHERE value")

                where_ = new_where

            if isinstance(where_, dict):
                for (key, values) in where_.items():
                    # parsing WHERE values

                    if not isinstance(values, list):
                        values = [values]

                    # Looking for equality or inequality
                    if len(values) > 1 and values[0] in [
                        "<", "<<", "<=",
                        ">=", ">>", ">",
                        "=", "==", "!=",
                        "<>",
                    ]:
                        operator = values.pop(0)

                        if len(values) == 1 and isinstance(
                                values[0], list
                        ):
                            values = values[0]
                    else:
                        operator = "="

                    stmt.request.script += f"({f'{operator}? OR '.join(key for _ in values)}{operator}? OR "
                    stmt.request.script = f"{stmt.request.script[:-3].strip()}) " + "AND "

                    if stmt.request.values:
                        if isinstance(stmt.request.values[0], tuple):
                            # if .values contains many values for insertmany stmt
                            # add where_ values for each value
                            new_values = list(stmt.request.values)

                            for i in range(len(new_values)):
                                new_values[i] = tuple(
                                    list(new_values[i]) + list(values)
                                )

                            stmt.request.values = tuple(new_values)

                        else:
                            # if .values contains only one set of values
                            # add where_ values
                            stmt.request.values = tuple(
                                list(stmt.request.values) + list(values)
                            )
                    else:
                        stmt.request.values = values

                stmt.request.script = stmt.request.script.strip()[:-3]

            elif isinstance(where_, str):
                stmt.request.script += f"{where_}"

            else:
                raise TypeError

            stmt.request.script = (
                f"{stmt.request.script.strip()}) "  # .strip() removing spaces around
            )

        return stmt

    return where_wrapper


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
        if "JOIN" in kwargs.keys():
            JOIN: JoinArgType = kwargs.pop("JOIN")
        else:
            JOIN: None = None

        stmt: SQLStatement = func(*args, **kwargs)

        if JOIN:
            if isinstance(JOIN, list):

                # if JOIN is not List[List] make it so
                if not isinstance(JOIN[0], list):
                    JOIN = [JOIN]

                for join_ in JOIN:
                    # If first element is JOIN type
                    if join_[0] in [INNER_JOIN, LEFT_JOIN, CROSS_JOIN]:
                        join_method = join_.pop(0)
                    else:
                        join_method = INNER_JOIN

                    # Adding JOIN to script
                    stmt.request.script += (
                        f"{join_method} {' '.join(j_arg for j_arg in join_)} "
                    )
            else:
                raise TypeError("Unexp")

        return stmt

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
        if "OR" in kwargs.keys():
            or_arg: OrOptionsType = kwargs.pop("OR")
        else:
            or_arg: None = None

        if or_arg:
            kwargs.update({"script": kwargs.get("script") + f" OR {or_arg}"})

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
        if "ORDER_BY" in kwargs.keys():
            order_by: OrderByType = kwargs.pop("ORDER_BY")
        else:
            order_by: None = None

        stmt: SQLStatement = func(*args, **kwargs)

        if order_by:
            if isinstance(order_by, (str, int)):
                stmt.request.script += f"ORDER BY {order_by} "
            elif isinstance(order_by, (list, tuple)):
                stmt.request.script += (
                    f"ORDER BY {', '.join(str(item_ob) for item_ob in order_by)} "
                )
            elif isinstance(order_by, dict):
                for (key, val) in order_by.items():
                    if isinstance(val, (str, int)):
                        uni_val = f"{val} "
                    elif isinstance(val, (list, tuple)):
                        uni_val = " ".join(sub_val for sub_val in val)
                    else:
                        raise TypeError

                    stmt.request.script += f"ORDER BY {key} {uni_val} "

        return stmt

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
        if "LIMIT" in kwargs.keys():
            limit: LimitOffsetType = kwargs.pop("LIMIT")
        else:
            limit: None = None

        stmt: SQLStatement = func(*args, **kwargs)

        if limit:
            if isinstance(limit, (float, str)):
                limit = int(limit)
            stmt.request.script += f"LIMIT {limit} "

        return stmt

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
        if "OFFSET" in kwargs.keys():
            offset: LimitOffsetType = kwargs.pop("OFFSET")
        else:
            offset: bool = False

        stmt: SQLStatement = func(*args, **kwargs)

        if offset:
            if isinstance(offset, (float, str)):
                offset = int(offset)
            stmt.request.script += f"OFFSET {offset} "

        return stmt

    return offset_wrapper





def args_parser(func: callable):
    """
    Decorator for parsing argument method.
    If func got only one argument which contains args for function it'll unwrap it

    if args is dict :
        return args = None, kwargs = args[0]

    if args is list :
        return args = args[0], kwargs = kwargs

    if args is tuple :
        return args = list(args[0]), kwargs = kwargs

    Parameters
    ----------
    func : callable
        SQLite3x method contains args

    Returns
    ----------
    callable
        Decorated method with parsed args
    """

    def args_parser_wrapper(*args: Any, **kwargs: Any):
        if not args:
            return func(*args, **kwargs)

        self = list(args)[0]
        args = list(args)[1:]

        if len(args) == 1:
            if isinstance(args[0], list):
                args = args[0]
            elif isinstance(args[0], (str, int)):
                args = [args[0]]
            elif isinstance(args[0], tuple):
                args = list(args[0])
            elif isinstance(args[0], dict):
                kwargs.update(args[0])
                args = []

        args = [self, *args]

        return func(*args, **kwargs)

    return args_parser_wrapper


__all__ = [
    'from_as_',
    'with_',
    'where_',
    'join_',
    'or_param_',
    'order_by_',
    'limit_',
    'offset_',

    'args_parser',
]
