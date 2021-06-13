from sqllex.exceptions import TableInfoError
from typing import Literal, Mapping, Union, List, AnyStr, Any, Tuple, Generator
from sqllex.debug import logger
from sqllex.constants.sql import *
from sqllex.types.types import *
import sqlite3


def col_types_sort(val: Union[DataType, AnyStr]) -> int:
    """
    Sorting function for DataType objects
    It's getting objects and returns index of priority (0,1,2,3)

    Parameters
    ----------
    val : Union[DataType, AnyStr]
        param of column type

    Returns
    -------
    int
        index of priority, if unknown returns 1

    """

    prior = CONST_PRIORITY.get(val)     # How about set dict.setdefault(1) ?

    if prior is None:
        return 1
    else:
        return prior


def __from_as__(func: callable):
    """
    Decorator for catching AS argument from TABLE arg

    Parameters
    ----------
    func : callable
        SQLite3x method where args might contain AS

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


def __with__(func: callable) -> callable:
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

        if with_dict:
            script = f"WITH RECURSIVE "
            values = []

            for (var, statement) in with_dict.items():

                # Checking is value of dict SQLStatement or str
                if issubclass(type(statement), SQLStatement):
                    condition = statement.request
                    script += f"{var} AS ({condition.script.strip()}), "  # .strip() removing spaces around
                    values += list(condition.values)

                elif isinstance(statement, str):
                    condition = statement
                    script += f"{var} AS ({condition}), "

                else:
                    raise TypeError(f"Unexpected type of WITH value\n"
                                    f"Got {type(statement)} instead of SQLStatement or str")

            if script[-2:] == ', ':
                script = script[:-2]

            kwargs.update(
                {
                    "values": tuple(values)
                    if not kwargs.get("values")
                    else tuple(list(kwargs.get("values")) + list(values)),

                    "script": f"{script} "
                    if not kwargs.get("script")
                    else f"{script} " + kwargs.get("script"),
                }
            )

        return func(*args, **kwargs)

    return with_wrapper


def __where__(func: callable) -> callable:
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

                    if not isinstance(values, list):
                        values = [values]

                    if len(values) > 1 and values[0] in [
                        "<", "<<", "<=", ">=",
                        ">>", ">", "=", "==",
                        "!=", "<>",
                    ]:
                        operator = values.pop(0)

                        if len(values) == 1 and isinstance(
                                values[0], list
                        ):
                            values = values[0]
                    else:
                        operator = "="

                    stmt.request.script += f"{f'{operator}? AND '.join(key for _ in values)}{operator}? AND "
                    stmt.request.values = tuple(
                        list(stmt.request.values) + list(values)
                    )

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


def __join__(func: callable) -> callable:
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


def __or_param__(func: callable) -> callable:
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


def __order_by__(func: callable) -> callable:
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


def __limit__(func: callable) -> callable:
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


def __offset__(func: callable) -> callable:
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


def __execute__(func: callable):
    """
    Decorator for execute SQLStatement
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def execute_wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                if stmt.request.values:
                    cur.execute(stmt.request.script, stmt.request.values)
                else:
                    cur.execute(stmt.request.script)

                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)
        stmt.request.script = stmt.request.script.strip()

        if not execute:
            return stmt

        logger.debug(
            f"\n"
            f"{stmt.request.script.strip()}\n"
            f"{stmt.request.values if stmt.request.values else ''}"
            f"\n"
        )

        # If connection does not exist
        if not stmt.connection:
            with sqlite3.connect(stmt.path) as conn:
                ret_ = executor(conn, stmt)
                conn.commit()
                return ret_
        else:
            return executor(stmt.connection, stmt)

    return execute_wrapper


def __executemany__(func: callable):
    """
    Decorator for execute SQLStatement with multiple values
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                cur.executemany(stmt.request.script, stmt.request.values)
                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)
        stmt.request.script = stmt.request.script.strip()

        if not execute:
            return stmt

        logger.debug(
            f"\n"
            f"{stmt.request.script.strip()}\n"
            f"{stmt.request.values if stmt.request.values else ''}"
            f"\n"
        )

        if not stmt.connection:
            with sqlite3.connect(stmt.path) as conn:
                ret_ = executor(conn, stmt)
                conn.commit()
                return ret_
        else:
            return executor(stmt.connection, stmt)

    return wrapper


def __executescript__(func: callable):
    """
    Decorator for execute SQLStatement with script only (without values)
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                cur.executescript(stmt.request.script)
                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)
        stmt.request.script = stmt.request.script.strip()

        if not execute:
            return stmt

        logger.debug(
            f"\n"
            f"{stmt.request.script.strip()}\n"
            f"{stmt.request.values if stmt.request.values else ''}"
            f"\n"
        )

        if not stmt.connection:
            with sqlite3.connect(stmt.path) as conn:
                ret_ = executor(conn, stmt)
                conn.commit()
                return ret_
        else:
            return executor(stmt.connection, stmt)

    return wrapper


def __update_constants__(func: callable) -> callable:
    """
    Decorator running method for update constants of class (self._update_instance_variables_())

    Used for updating columns list in SQLite3xTable class

    Parameters
    ----------
    func : callable
        Class method after witch needed to update constants

    Returns
    ----------
    callable
        Decorated method with update after it was run

    """

    def wrap(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self._update_instance_variables_()
        return res

    return wrap


def lister(data: Any, remove_one_len: bool = False) -> List:
    """
    Function converting input value from Tuple[Any] or List[Tuple]
    (with any deepness) to List[List]

    Parameters
    ----------
    data : Any
        Any value contains tuples
    remove_one_len : bool
        Convert or not [['x'], 1] to ['x', 1] (breaking return rule)

    Returns
    ----------
    callable
        Decorated method with update after it was run

    """

    if isinstance(data, tuple):
        data = list(data)

    if isinstance(data, list):
        if remove_one_len and (len(data) == 1):
            return lister(
                data[0],
                remove_one_len
            )

        for r in range(len(data)):
            if isinstance(data[r], (list, tuple)):
                data[r] = lister(
                    data[r],
                    remove_one_len
                )

    return data


def tuples_to_lists(func: callable) -> callable:
    """
    Decorator converting returning data to List[List]

    Parameters
    ----------
    func : callable
        Function or method returns of with one need to convert from Tuple[Tuple[Any]] to List[List[Any]]

    Returns
    ----------
    callable
        Decorated method or func returning List[List]

    """

    def t2l_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        if not issubclass(ret.__class__, SQLStatement):
            ret = lister(ret)

            if not isinstance(ret, list):
                ret = [ret]

        return ret

    return t2l_wrapper


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

    def wrapper(*args: Any, **kwargs: Any):
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

    return wrapper


def crop(columns: Union[Tuple, List], values: Union[Tuple, List]) -> Tuple:
    """
    Converts input lists (columns and values) to the same length for safe insert

    Parameters
    ----------
    columns : Union[Tuple, List]
        List of columns in some table
    values : Union[Tuple, List]
        Values for insert to some table

    Returns
    ----------
        Equalized by length lists

    """

    if values and columns:
        if len(values) != len(columns):
            logger.debug(
                f"\n"
                f"SIZE CROP! Expecting {len(columns)} arguments but {len(values)} were given!\n"
                f"Expecting: {columns}\n"
                f"Given: {values}"
            )
            _len_ = min(len(values), len(columns))
            return columns[:_len_], values[:_len_]

    return columns, values


class SQLite3xTable:
    """
    Sub-class of SQLite3x contains one table of Database
    Have same methods but without table name argument

    Attributes
    ----------
    db : SQLite3x
        SQLite3x database object
    name : str
        Name of table
    columns : list
        List of columns in table (auto-updating)

    """

    def __init__(self, db, name: AnyStr):
        """
        Parameters
        ----------
        db : SQLite3x
            SQLite3x database object
        name : str
            Name of table

        """
        self.db: SQLite3x = db
        self.name: AnyStr = name
        self.columns: List = self.get_columns()

    def __str__(self):
        return f"{{SQLite3x Table: name: '{self.name}', db: '{self.db}'}}"

    def __bool__(self):
        return bool(self.get_columns())

    def __getitem__(self, key) -> List:
        if key not in self.get_columns():
            raise KeyError(key, "No such column in table")

        return self.select(key)

    def _update_constants_(self):
        """
        Update classes vars (columns)

        """
        self.columns = self.get_columns()

    def info(self):
        """
        Send PRAGMA request table_info(table_name)

        Returns
        ----------
        list
            All information about table

        """

        return self.db.pragma(f"table_info({self.name})")

    def get_columns(self) -> List:
        """
        Get list of table columns

        Returns
        ----------
        List[List]
            All table's columns

        """
        return self.db.get_columns(table=self.name)

    def insert(
            self,
            *args: InsertData,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        INSERT data into table

        Parameters
        ----------
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        WITH : WithType
            Optional parameter.
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
            None or SQL-script in SQLStatement
        """

        return self.db.insert(
            self.name, *args, OR=OR, execute=execute, WITH=WITH, **kwargs
        )

    def replace(
            self,
            *args: Any,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs: Any
    ) -> Union[None, SQLStatement]:
        """
        REPLACE data into table

        Parameters
        ----------
        WITH : WithType
            Optional parameter.
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        return self.db.replace(self.name, *args, execute=execute, **kwargs, WITH=WITH)

    def insertmany(
            self,
            *args: Union[List[InsertData], Tuple[InsertData]],
            OR: OrOptionsType = None,
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        Parameters
        ----------
        args : Union[List, Tuple]
            1'st way set values for insert
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        return self.db.insertmany(self.name, *args, OR=OR, execute=execute, **kwargs)

    def select(
            self,
            *args: Union[str, List[str]],
            SELECT: Union[str, List[str]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            execute: bool = True,
            **kwargs,
    ) -> Union[SQLStatement, List[List[Any]]]:
        """
        SELECT data from table

        Parameters
        ----------
        *args: Union[str, List[str]]
            selecting column or list of columns
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
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
        List[List]
            selected data

        """

        return self.db.select(
            self.name,
            *args,
            SELECT=SELECT,
            WHERE=WHERE,
            execute=execute,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def select_distinct(
            self,
            SELECT: Union[List[str], str] = ALL,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        return self.db.select_distinct(
            self.name,
            SELECT=SELECT,
            WHERE=WHERE,
            execute=execute,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            **kwargs,
        )

    def select_all(
            self,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        """
        SELECT data from table

        Parameters
        ----------
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
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
        List[List]
            selected data

        """

        return self.db.select_all(
            self.name,
            execute=execute,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            **kwargs,
        )

    def delete(
            self,
            WHERE: WhereType = None,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs,
    ) -> Union[None, SQLStatement]:
        """
        DELETE FROM table WHERE {something}

        Parameters
        ----------
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        WITH : WithType
            with_statement (don't really work well)
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        """

        return self.db.delete(
            self.name, WHERE=WHERE, WITH=WITH, execute=execute, **kwargs
        )

    def update(
            self,
            SET: Union[List, Tuple, Mapping],
            WHERE: WhereType = None,
            OR: OrOptionsType = None,
            execute: bool = True,
            WITH: WithType = None,
            **kwargs,
    ):
        """
        UPDATE, SET column_name=something WHERE x=y and more complex requests

        Parameters
        ----------
        SET : Union[List, Tuple, Mapping]
            Column and value to set
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        WITH : WithType
            with_statement (don't really work well)
        """

        return self.db.update(
            self.name, SET=SET, OR=OR, WHERE=WHERE, execute=execute, WITH=WITH, **kwargs
        )

    def drop(self, IF_EXIST: bool = True, execute: bool = True, **kwargs):
        """
        DROP TABLE (IF EXIST)

        Parameters
        ----------
        IF_EXIST : bool
            Check is table exist (boolean)
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        """

        self.db.drop(self.name, IF_EXIST=IF_EXIST, execute=execute, **kwargs)

    def find(
            self,
            WHERE: WhereType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        """
        Find all records in table where

        Parameters
        ----------
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        ORDER_BY : OrderByType
            optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
        LIMIT : LimitOffsetType
            optional parameter for conditions, example: 10
        **kwargs :

        Returns
        ----------
        List[List]
            selected data
        """
        if not WHERE:
            WHERE = kwargs

        return self.select_all(WHERE=WHERE, ORDER_BY=ORDER_BY, LIMIT=LIMIT)


class SQLite3x:
    """
    Main SQLite3x Database Class

    Attributes
    ----------
    connection : Union[sqlite3.Connection, None]
        SQLite connection
    path : PathType
        Local path to database (PathType)
    template : DBTemplateType
        template of database structure (DBTemplateType)


    """

    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        Initialization

        Parameters
        ----------
        path : PathType
            Local path to database (PathType)
        template : DBTemplateType
            template of database structure (DBTemplateType)

        """
        self.connection: Union[sqlite3.Connection, None] = None
        self.path = path
        self.tables = self._get_tables_()
        self.tables_names = self._get_tables_names_()
        self.journal_mode(mode="WAL")  # make db little bit faster
        self.foreign_keys(mode="ON")
        if template:
            self.markup(template=template)

    def __str__(self):
        return f"{{SQLite3x: path='{self.path}'}}"

    def __bool__(self):
        try:
            return bool(self.pragma("database_list"))
        except Exception as error:
            logger.error(error)
            return False

    def __getitem__(self, key) -> SQLite3xTable:
        # To call method down below is necessary,
        # otherwise it might fall in case of multiple DB objects
        self._update_instance_variables_()

        if key not in self.tables_names:
            raise KeyError(key, "No such table in database",
                           f"Available tables: {self.tables_names}")

        return SQLite3xTable(db=self, name=key)

    def __del__(self):
        if self.connection:
            self.disconnect()

    # ============================== PRIVATE METHODS ==============================

    def _update_instance_variables_(self):
        """
        Method to update (changed) instance variables

        """
        self.tables_names = self._get_tables_names_()
        self.tables = self._get_tables_()

    def _get_tables_(self) -> Generator[SQLite3xTable, None, None]:
        """
        Generator of tables list

        Yield
        ----------
        SQLite3xTable
            Tables list

        """

        # Code down below commented because I guess it's better to see all tables
        # even Internal SQLite tables. Might be changed later
        #
        # if "sqlite_sequence" in table_names:
        #     table_names.remove("sqlite_sequence")

        for tab_name in self.tables_names:
            yield self.__getitem__(tab_name)
            # tables.append(self.__getitem__(tab_name))

        # line down below it is necessary for possibility to call self.tables unlimited times
        # make it never end, because in the end of generation it'll be overridden
        self.tables = self._get_tables_()

    def _get_tables_names_(self) -> List[str]:
        """
        Get list of tables names from database

        Returns
        ----------
        List[str]
            list of tables names

        """

        return lister(
            self.execute("SELECT name FROM sqlite_master WHERE type='table'"),
            remove_one_len=True
        )

    @tuples_to_lists
    @__execute__
    def _execute_stmt_(
            self, script: AnyStr = None, values: Tuple = None, request: SQLRequest = None
    ):
        """
        Parent method for execute
        """

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path, self.connection)
        else:
            return SQLStatement(request, self.path, self.connection)

    @tuples_to_lists
    @__executemany__
    def _executemany_stmt(
            self, script: AnyStr = None, values: Tuple = None, request: SQLRequest = None
    ):
        """
        Parent method for executemany
        """

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path, self.connection)
        else:
            return SQLStatement(request, self.path, self.connection)

    @tuples_to_lists
    @__executescript__
    def _executescript_stmt(
            self, script: AnyStr = None, values: Tuple = None, request: SQLRequest = None
    ):
        """
        Parent method for executescript
        """

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path, self.connection)
        else:
            return SQLStatement(request, self.path, self.connection)

    @tuples_to_lists
    @__execute__
    def _pragma_stmt_(self, *args: str, **kwargs):
        """
        Parent method for all pragma-like methods
        """

        if args:
            script = f"PRAGMA {args[0]}"
        elif kwargs:
            script = f"PRAGMA {list(kwargs.keys())[0]}={list(kwargs.values())[0]}"
        else:
            raise ValueError(f"No data to execute, args: {args}, kwargs: {kwargs}")

        return SQLStatement(SQLRequest(script), self.path, self.connection)

    @__update_constants__
    @__execute__
    def _create_stmt_(
            self,
            temp: AnyStr,
            name: AnyStr,
            columns: ColumnsType,
            IF_NOT_EXIST: bool = None,
            without_rowid: bool = None,
    ):
        """
        Parent method for all CREATE-like methods
        """

        content = ""
        values = ()

        for (col, params) in columns.items():

            # For {'col': 'params'} -> {'col': ['params']}
            if isinstance(params, str):
                params = [f"{params} "]

            # For {'col': [param2, param1]} -> {'col': [param1, param2]}
            if isinstance(params, list):
                params = sorted(params, key=lambda par: col_types_sort(par))
                content += f"{col} {' '.join(str(param) for param in params)},\n"

            # For {'col': {FK: {a: b}}}
            elif isinstance(params, dict) and col == FOREIGN_KEY:
                res = ""
                for (key, refs) in params.items():
                    res += (
                        f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
                    )
                content += res[:-1]

            else:
                raise TypeError

        content = f"{content[:-2]}"

        script = (
            f"CREATE "
            f"{temp} "
            f"TABLE "
            f"{'IF NOT EXISTS' if IF_NOT_EXIST else ''} "
            f"'{name}' "
            f" (\n{content}\n) "
            f"{'WITHOUT ROWID' if without_rowid else ''};"
        )

        return SQLStatement(
            SQLRequest(script=script, values=values), self.path, self.connection
        )

    @__execute__
    @__or_param__
    @__with__
    @__from_as__
    @args_parser
    def _insert_stmt_(
            self, *args: Any, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for INSERT-like methods

        INSERT INTO request (aka insert-stmt) and REPLACE INTO request

        """

        # parsing args or kwargs for _columns and insert_values
        if args:
            _columns = self.get_columns(table=TABLE)
            _columns, args = crop(_columns, args)
            insert_values = args

        elif kwargs:
            _columns = tuple(kwargs.keys())
            insert_values = list(kwargs.values())

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        script += (
            f"{' ' if script else ''}"
            f"INTO {TABLE} ("
            f"{', '.join(column for column in _columns)}) "
            f"VALUES ("
            f"{', '.join('?' * len(insert_values))}) "
        )

        all_values = tuple(values) + tuple(insert_values)

        return SQLStatement(
            SQLRequest(script, tuple(value for value in all_values)),
            self.path,
            self.connection,
        )

    @__execute__
    @__or_param__
    @__with__
    @__from_as__
    @args_parser
    def _fast_insert_stmt_(
            self, *args, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for fast INSERT-like methods

        'INSERT INTO' request and 'REPLACE INTO' request without columns names
        (without get_columns req because it's f-g slow)
        """

        if not args:
            raise sqlite3.OperationalError

        script += (
            f"{' ' if script else ''}"
            f"INTO {TABLE} "
            f"VALUES ("
            f"{', '.join('?' * len(args))}) "
        )

        values = tuple(list(values) + list(args))

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @__executemany__
    @__or_param__
    @__from_as__
    @args_parser
    def _insertmany_stmt_(
            self,
            TABLE: AnyStr,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            script="",
            values=(),
            **kwargs: Any,
    ):
        """
        Parent method for insertmany method

        """

        if args:
            values = list(
                map(lambda arg: list(arg), args)
            )

            if len(values) == 1 and isinstance(values[0], list):
                values = values[0]

            max_l = max(map(lambda arg: len(arg), values))  # max len of arg in values
            temp_ = [0 for _ in range(max_l)]  # example values [] for script
            stmt = self._insert_stmt_(temp_, script="INSERT", TABLE=TABLE,
                                      execute=False)  # getting stmt for maxsize value
            _len = len(stmt.request.values)  # len of max supported val list

            for i in range(len(values)):  # cropping or appending values, making it's needed size
                while len(values[i]) < _len:
                    values[i] += [None]
                if len(values[i]) > _len:
                    values[i] = values[i][:_len]

        elif kwargs:
            temp_ = {}
            values = []
            columns = list(kwargs.keys())
            args = list(map(lambda vals: list(vals), kwargs.values()))

            for i in range(len(args)):
                try:
                    temp_[columns[i]] = args[i][0]
                except IndexError:
                    temp_[columns[i]] = None

            stmt = self._insert_stmt_(temp_, script="INSERT", TABLE=TABLE,
                                      execute=False)  # getting stmt for maxsize value
            max_l = max(map(lambda val: len(val), args))  # max len of arg in values

            for _ in range(max_l):
                temp_ = []
                for arg in args:
                    if arg:
                        temp_.append(arg.pop(0))
                    else:
                        temp_.append(None)
                values.append(temp_)

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        values = tuple(
            map(lambda arg: tuple(arg), values)
        )  # make values tuple[tuple] (yes it's necessary)

        return SQLStatement(
            SQLRequest(stmt.request.script, values), self.path, self.connection
        )

    @tuples_to_lists
    @__execute__
    @__offset__
    @__limit__
    @__order_by__
    @__where__
    @__join__
    @__with__
    @__from_as__
    def _select_stmt_(
            self,
            TABLE: str,
            script="",
            values=(),
            method: AnyStr = "SELECT ",
            SELECT: Union[List[str], str] = None,
    ):
        """
        Parent method for all SELECT-like methods

        """
        if not TABLE:
            raise ValueError("Argument TABLE unset and have not default value")

        if SELECT is None:
            if method != "SELECT ALL ":
                logger.warning("Argument SELECT not specified, default value is '*'")
            SELECT = ["*"]

        elif isinstance(SELECT, str):
            SELECT = [SELECT]

        script += f"{method} " f"{', '.join(sel for sel in SELECT)} " f"FROM {TABLE} "

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @__execute__
    @__where__
    @__with__
    def _delete_stmt_(self, TABLE: str, script="", values=()):
        """
        Parent method for delete method

        """

        script += f"DELETE FROM {TABLE} "
        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @__execute__
    @__where__
    @__or_param__
    @__with__
    def _update_stmt_(
            self,
            TABLE: AnyStr,
            SET: Union[List, Tuple, Mapping] = None,
            script="",
            values=(),
            **kwargs,
    ):
        """
        Parent method for update method

        """

        set_ = SET if SET else None

        if not set_ and kwargs:
            set_ = kwargs

        if isinstance(set_, tuple):
            set_ = list(set_)

        if isinstance(set_, list):
            new_set = {}

            if len(set_) % 2 == 0:  # for ['name', 'Alex', 'age', 2]
                for i in range(len(set_) // 2):
                    new_set.update({set_[2 * i]: set_[2 * i + 1]})

            else:
                raise TypeError

            set_ = new_set

        values = tuple(list(values) + list(set_.values()))

        script += (
            f"UPDATE {TABLE} " f"SET {'=?, '.join(s for s in list(set_.keys()))}=? "
        )

        return SQLStatement(
            SQLRequest(script=script, values=values), self.path, self.connection
        )

    @__update_constants__
    @__execute__
    def _drop_stmt_(
            self,
            TABLE: AnyStr,
            IF_EXIST: bool = True,
            script="",
            **kwargs
    ):
        """
        Parent method for drop method

        """

        script += f"DROP TABLE {'IF EXISTS' if IF_EXIST else ''} {TABLE} "
        return SQLStatement(SQLRequest(script=script), self.path, self.connection)

    # ============================== PUBLIC METHODS ==============================

    def connect(self):
        """
        Create connection to database

        Creating sqlite3.connect(path) connection to interact with database

        """

        if not self.connection:
            self.connection = sqlite3.connect(self.path)

        # Not sure is this reasonable
        # return self.connection

    def disconnect(self):
        """
        Drop connection to database

        Commit changes and close connection

        """

        self.connection.commit()
        self.connection.close()
        self.connection = None

    def get_table(self, name: AnyStr) -> SQLite3xTable:
        """
        Shadow method for __getitem__, that used as like: database['table_name']

        Get table object (SQLite3xTable instance)

        Parameters
        ----------
        name : AnyStr
            Name of table

        Returns
        ----------
        SQLite3xTable
            Instance of SQLite3xTable, table of database

        """

        return self.__getitem__(key=name)

    def execute(
            self,
            script: AnyStr = None,
            values: Tuple = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Execute any SQL-script whit (or without) values, or execute SQLRequest

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains placeholders
        values : Tuple
            Values for placeholders if script contains it
        request : SQLRequest
            Instead of script and values might execute full statement

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._execute_stmt_(script=script, values=values, request=request)

    def executemany(
            self,
            script: AnyStr = None,
            values: Tuple[Tuple] = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Execute any SQL-script for many values sets, or execute SQLRequest

        Parameters
        ----------
        script : AnyStr
            single or multiple SQLite script(s), might contains placeholders
        values : Tuple[Tuple]
            Values for placeholders if script contains it
        request : SQLRequest
            Instead of script and values might execute full request

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._executemany_stmt(script=script, values=values, request=request)

    def executescript(
            self,
            script: AnyStr = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Execute many SQL-scripts whit (or without) values

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains placeholders
        request : SQLRequest
            Instead of script and values might execute full statement

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._executescript_stmt(script=script, request=request)

    def pragma(
            self,
            *args: str,
            **kwargs: NumStr
    ) -> Union[List, None]:
        """
        Set PRAGMA parameter or send PRAGMA-request

        Parameters
        ----------
        args : str
            Might be used like this:
            Example: db.pragma("database_list")
        kwargs : NumStr
            Might be used like this:
            Example: db.pragma(foreign_keys="ON")

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._pragma_stmt_(*args, **kwargs)

    def foreign_keys(
            self,
            mode: Literal["ON", "OFF"]
    ):
        """
        Turn on/off PRAGMA parameter FOREIGN KEYS

        Parameters
        ----------
        mode : Literal["ON", "OFF"]
            "ON" or "OFF" FOREIGN KEYS support

        """

        return self.pragma(foreign_keys=mode)

    def journal_mode(
            self,
            mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
    ):
        """
        Set PRAGMA param journal_mode

        Parameters
        ----------
        mode : Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
            Journal mode

        """

        return self.pragma(journal_mode=mode)

    def table_info(
            self,
            table_name: str
    ):
        """
        Send table_info PRAGMA request

        table_name : str
            Name of table

        """

        return self.pragma(f"table_info({table_name})")

    def create_table(
            self,
            name: AnyStr,
            columns: ColumnsType,
            IF_NOT_EXIST: bool = None,
            without_rowid: bool = None,
    ):
        """
        Method to create new table

        Parameters
        ----------
        name : AnyStr
            Name of creating table
        columns : ColumnsType
            Columns of table (ColumnsType-like)
        IF_NOT_EXIST :
            Turn on/off "IF NOT EXISTS" prefix
        without_rowid :
            Turn on/off "WITHOUT ROWID" postfix

        """

        self._create_stmt_(
            temp="",
            name=name,
            columns=columns,
            IF_NOT_EXIST=IF_NOT_EXIST,
            without_rowid=without_rowid,
        )

    @__update_constants__
    def create_temp_table(
            self,
            name: AnyStr,
            columns: ColumnsType,
            **kwargs
    ):
        """
        CREATE TEMP TABLE (IF NOT EXISTS) schema-name.table-name ...
        (AS select-stmt)/(column-def table-constraint) (WITHOUT ROWID)

        Parameters
        ----------
        name : AnyStr
            Name of creating table
        columns : ColumnsType
            Columns of table (ColumnsType-like)
        kwargs : Any
            Other optional kwargs

        """

        self._create_stmt_(
            temp="TEMP",
            name=name,
            columns=columns,
            **kwargs
        )

    @__update_constants__
    def create_temporary_table(
            self,
            name: AnyStr,
            columns: ColumnsType,
            **kwargs
    ):
        """
        CREATE TEMPORARY TABLE (IF NOT EXISTS) schema-name.table-name ...
        (AS select-stmt)/(column-def table-constraint) (WITHOUT ROWID)

        Parameters
        ----------
        name : AnyStr
            Name of creating table
        columns : ColumnsType
            Columns of table (ColumnsType-like)
        kwargs : Any
            Other optional kwargs

        """

        self._create_stmt_(
            temp="TEMPORARY",
            name=name,
            columns=columns,
            **kwargs
        )

    @__update_constants__
    def markup(
            self,
            template: DBTemplateType
    ):
        """
        Mark up table structure from template

        Parameters
        ----------
        template : DBTemplateType
            Template of database structure (DBTemplateType-like)

        """

        for (table_name, columns) in template.items():
            self.create_table(
                name=table_name,
                columns=columns,
                IF_NOT_EXIST=True
            )

    def get_columns(
            self,
            table: AnyStr
    ) -> List[str]:
        """
        Get list of table columns

        Parameters
        ----------
        table : AnyStr
            Name of table

        Returns
        ----------
        List[List]
            Columns of table

        """

        try:
            columns_: List[List[str]] = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")
            columns: List[str] = list(map(lambda item: item[0], columns_))

        except sqlite3.OperationalError:
            # Fix for compatibility issues #19, by some reason it can't find PRAGMA_TABLE_INFO table
            columns_: List[List[str]] = self.pragma(f"table_info('{table}')")
            columns: List[str] = list(map(lambda item: item[1], columns_))

        if not columns:
            raise TableInfoError

        return columns

    def insert(
            self,
            TABLE: AnyStr,
            *args: InsertData,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        INSERT data into table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        WITH : WithType
            Optional parameter.
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
            None or SQL-script in SQLStatement
        """

        if args:
            try:
                return self._fast_insert_stmt_(
                    *args,
                    script="INSERT",
                    OR=OR,
                    TABLE=TABLE,
                    execute=execute,
                    **kwargs,
                    WITH=WITH,
                )
            except sqlite3.OperationalError:
                pass

        return self._insert_stmt_(
            *args,
            script="INSERT",
            OR=OR,
            TABLE=TABLE,
            execute=execute,
            **kwargs,
            WITH=WITH,
        )

    def replace(
            self,
            TABLE: AnyStr,
            *args: Any,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        REPLACE data into table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        WITH : WithType
            Optional parameter.
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        if args:
            try:
                return self._fast_insert_stmt_(
                    *args,
                    script="REPLACE",
                    TABLE=TABLE,
                    execute=execute,
                    **kwargs,
                    WITH=WITH,
                )
            except sqlite3.OperationalError:
                pass

        return self._insert_stmt_(
            *args,
            script="REPLACE",
            TABLE=TABLE,
            execute=execute,
            **kwargs,
            WITH=WITH
        )

    def insertmany(
            self,
            TABLE: AnyStr,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            OR: OrOptionsType = None,
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        args : Union[List, Tuple]
            1'st way set values for insert
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        return self._insertmany_stmt_(
            TABLE,
            *args,
            OR=OR,
            execute=execute,
            **kwargs
        )

    def select(
            self,
            TABLE: Union[str, List[str]] = None,
            *args: Union[str, List[str]],
            SELECT: Union[str, List[str]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            FROM: Union[str, List[str]] = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[SQLStatement, List[Any]]:
        """
        SELECT data from table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        *args: Union[str, List[str]]
            selecting column or list of columns
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
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        FROM : str
            Name of table, same at TABLE
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],

        Returns
        ----------
        List[List]
            selected data

        """

        if not TABLE:
            if FROM:
                TABLE = FROM
            else:
                raise ValueError("No TABLE or FROM argument set")

        if not SELECT:
            if args:
                if isinstance(list(args)[0], list):
                    SELECT = list(args)[0]
                else:
                    SELECT = list(args)
            else:
                SELECT = ALL

        if not WHERE:
            WHERE = kwargs
            kwargs = {}

        return self._select_stmt_(
            SELECT=SELECT,
            TABLE=TABLE,
            method="SELECT",
            WHERE=WHERE,
            execute=execute,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def select_distinct(
            self,
            TABLE: Union[str, List[str]] = None,
            *args: Union[str, List[str]],
            SELECT: Union[str, List[str]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            FROM: Union[str, List[str]] = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:

        if not TABLE:
            if FROM:
                TABLE = FROM
            else:
                raise ValueError("No TABLE or FROM argument set")

        if not SELECT:
            if args:
                if isinstance(list(args)[0], list):
                    SELECT = list(args)[0]
                else:
                    SELECT = list(args)
            else:
                SELECT = ALL

        if not WHERE:
            WHERE = kwargs
            kwargs = {}

        return self._select_stmt_(
            SELECT=SELECT,
            TABLE=TABLE,
            method="SELECT DISTINCT",
            WHERE=WHERE,
            execute=execute,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            **kwargs,
        )

    def select_all(
            self,
            TABLE: Union[str, List[str]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            FROM: Union[str, List[str]] = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        """
        SELECT ALL records from table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
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
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        FROM : str
            Name of table, same at TABLE

        Returns
        ----------
        List[List]
            selected data

        """

        if not TABLE:
            if FROM:
                TABLE = FROM
            else:
                raise ValueError("No TABLE or FROM argument set")

        if not WHERE:
            WHERE = kwargs
            kwargs = {}

        return self._select_stmt_(
            method="SELECT ALL ",
            execute=execute,
            TABLE=TABLE,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            **kwargs,
        )

    def delete(
            self,
            TABLE: str,
            WHERE: WhereType = None,
            WITH: WithType = None,
            execute: bool = True,
            **kwargs,
    ) -> Union[None, SQLStatement]:
        """
        DELETE FROM table WHERE {something}

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        WITH : WithType
            with_statement (don't really work well)
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object

        """

        if not WHERE:
            WHERE = kwargs

        return self._delete_stmt_(
            TABLE=TABLE,
            WHERE=WHERE,
            WITH=WITH,
            execute=execute
        )

    def update(
            self,
            TABLE: AnyStr,
            SET: Union[List, Tuple, Mapping],
            WHERE: WhereType = None,
            OR: OrOptionsType = None,
            execute: bool = True,
            WITH: WithType = None,
            **kwargs,
    ):
        """
        UPDATE, SET column_name=something WHERE x=y and more complex requests

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        SET : Union[List, Tuple, Mapping]
            Column and value to set
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        WITH : WithType
            with_statement (don't really work well)
        """

        if not WHERE:
            WHERE = kwargs

        return self._update_stmt_(
            TABLE=TABLE,
            SET=SET,
            OR=OR,
            WHERE=WHERE,
            execute=execute,
            WITH=WITH,
            **kwargs,
        )

    def drop(
            self,
            TABLE: AnyStr,
            IF_EXIST: bool = True,
            execute: bool = True,
            **kwargs
    ):
        """
        DROP TABLE (IF EXIST)

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        IF_EXIST : bool
            Check is table exist (boolean)
        execute : bool
            if True: execute script and return db's answer
            if False: return SQL-script in SQLStatement object
        """

        return self._drop_stmt_(
            TABLE=TABLE,
            IF_EXIST=IF_EXIST,
            execute=execute,
            **kwargs
        )


__all__ = ["SQLite3x", "SQLite3xTable"]
