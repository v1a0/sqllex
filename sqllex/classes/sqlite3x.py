from sqllex.exceptions import TableInfoError, ArgumentError, ExecuteError
from typing import Literal, Mapping, Union, List, AnyStr, Any, Tuple, Generator
from sqllex.debug import logger
from sqllex.constants.sql import *
from sqllex.types.types import *
import sqlite3


def col_types_sort(val: Union[DataType, AnyStr]) -> int:
    """
    Func for lambda func sorting DataTypes of columns

    :param val: DataType or AnyStr : param of column type
    :return: index of priority, if unknown returns 1
    """

    prior = CONST_PRIORITY.get(val)

    if prior is None:
        return 1
    else:
        return prior


def __from_as__(func: callable):
    """
    Decorator for catching AS argument from TABLE arg

    :param func: SQLite3x method where args might contain AS
    :return: Decorated method with TABLE arg as string (instead list with AS)
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

    :param func: SQLite3x method contains arg WITH
    :return: Decorated method with script contains with_statement and values contains values of with_statement
    """

    def with_wrapper(*args, **kwargs):
        if "WITH" in kwargs.keys():
            with_dict: WithType = kwargs.pop("WITH")
        else:
            with_dict: None = None

        if with_dict:
            script = f"WITH "
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
                    raise TypeError

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

    :param func: SQLite3x method contains arg WHERE
    :return: Decorated method with script contains where_statement and values contains values of where_statement
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
                        raise TypeError

                where_ = new_where

            if isinstance(where_, dict):
                for (key, values) in where_.items():
                    if not isinstance(values, list):
                        values = [values]

                    if len(values) > 1 and values[0] in [
                        "<",
                        "<<",
                        "<=",
                        ">=",
                        ">>",
                        ">",
                        "=",
                        "==",
                        "!=",
                        "<>",
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

    :param func: SQLite3x method contains arg JOIN
    :return: Decorated method with script contains join_statement and values contains values of join_statement
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
                raise TypeError

        return stmt

    return join_wrapper


def __or_param__(func: callable) -> callable:
    """
    Decorator for catching OR argument in kwargs of method

    If it has, adding into beginning of :SQLStatement.script: or_statement.
    And adding values into :SQLStatement.values: if it has.

    :param func: SQLite3x method contains arg JOIN
    :return: Decorated method with script contains or_statement and values contains values of or_statement
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

    :param func: SQLite3x method contains arg ORDER BY
    :return: Decorated method with script contains order_by_statement and values contains values of order_by_statement
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

    :param func: SQLite3x method contains arg LIMIT
    :return: Decorated method with script contains limit_statement and values contains values of limit_statement
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

    :param func: SQLite3x method contains arg OFFSET
    :return: Decorated method with script contains offset_statement and values contains values of offset_statement
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

    :param func: SQLite3x method
    :return: Database answer (if execute True) or SQLStatement (if execute False) or None
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

    :param func: SQLite3x method
    :return: Database answer (if execute True) or SQLStatement (if execute False) or None
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

    :param func: SQLite3x method
    :return: Database answer (if execute True) or SQLStatement (if execute False) or None
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
    Decorator running method for update constants of class (self._update_constants_())

    Used for updating columns list in SQLite3xTable class

    :param func: Class method after witch needed to update constants
    :return: Decorated method with update after it was run
    """

    def wrap(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self._update_constants_()
        return res

    return wrap


def lister(value: Any):
    """
    Function converting input value from
    Tuple[Any] or List[Tuple] with any deepness to List[List]

    :param value: Any value contains tuples
    :return: Decorated method with update after it was run
    """

    if isinstance(value, tuple):
        value = list(value)

    if isinstance(value, list):
        if len(value) == 1:
            return lister(value[0])

        for r in range(len(value)):
            if isinstance(value[r], (list, tuple)):
                value[r] = lister(value[r])

    return value


def tuples_to_lists(func: callable) -> callable:
    """
    Decorator converting returning data to List[List]

    :param func: Function or method returns of with one need to convert
    :return: Decorated method or func returning List[List]
    """

    def t2l_wrapper(*args, **kwargs):
        ret = lister(func(*args, **kwargs))

        if not issubclass(ret.__class__, SQLStatement):
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

    :param func: SQLite3x method contains args
    :return: Decorated method with parsed args
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

    :param columns: List of columns in some table
    :param values: Values for insert to some table
    :return: Equalized by length lists
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

    """

    def __init__(self, db, name: AnyStr):
        self.db: SQLite3x = db
        self.name = name
        self.columns = self.get_columns()

    def __str__(self):
        return f"{{SQLite3x Table: name: '{self.name}', db: '{self.db}'}}"

    def __bool__(self):
        return bool(self.get_columns())

    def __getitem__(self, key) -> List:
        if key not in self.get_columns():
            raise KeyError(key, "No such column in table")

        return self.select(key)

    def _update_constants_(self):
        self.columns = self.get_columns()

    def info(self):
        """
        Send PRAGMA request table_info(table_name)

        :return: table info
        """

        return self.db.pragma(f"table_info({self.name})")

    def get_columns(self) -> Union[Tuple, List]:
        """
        Get list of table columns

        :return: List[List] of columns
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

        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param WITH: Optional parameter.
        :param execute: execute script and return db's answer (True) or return script (False)
        """

        return self.db.insert(
            self.name, *args, OR=OR, execute=execute, WITH=WITH, **kwargs
        )

    def replace(
            self, *args: Any, WITH: WithType = None, execute: bool = True, **kwargs: Any
    ) -> Union[None, SQLStatement]:
        """
        REPLACE data into table

        :param WITH: Optional parameter.
        :param execute: execute script and return db's answer (True) or return script (False)
        """

        return self.db.replace(self.name, *args, execute=execute, **kwargs, WITH=WITH)

    def insertmany(
            self,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            execute: bool = True,
            **kwargs: Any,
    ) -> Union[None, SQLStatement]:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        :param execute: execute script and return db's answer (True) or return script (False)
        :param args: 1'st way set values for insert
        :param kwargs: 2'st way set values for insert
        """

        return self.db.insertmany(self.name, *args, execute=execute, **kwargs)

    def select(
            self,
            SELECT: Union[str, List[str]] = ALL,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[SQLStatement, List[Any]]:
        """
        SELECT data from table

        :param SELECT: columns to select. Value '*' by default
        :param WHERE: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        :param WITH: with_statement
        :param JOIN: optional parameter for joining data from other tables ['groups'],
        :param ORDER_BY: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
        :param LIMIT: optional parameter for conditions, example: 10
        :param OFFSET: optional parameter for conditions, example: 5
        :param execute: execute script and return db's answer (True) or return script (False)

        :return: List[List] of selects
        """

        return self.db.select(
            self.name,
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

        :param WHERE: where_statement
        :param WITH: with_statement
        :param execute: execute script and return db's answer (True) or return script (False)
        """

        return self.db.delete(
            self.name, WHERE=WHERE, WITH=WITH, execute=execute, **kwargs
        )

    def update(
            self,
            SET: Union[List, Tuple, Mapping],
            WHERE: WhereType,
            OR: OrOptionsType = None,
            execute: bool = True,
            WITH: WithType = None,
            **kwargs,
    ):
        """
        UPDATE, SET column_name=something WHERE x=y and more complex requests

        :param SET: Column and value to set
        :param WHERE: where_statement
        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param execute: execute script and return db's answer (True) or return script (False)
        :param WITH: with_statement
        """

        return self.db.update(
            self.name, SET=SET, OR=OR, WHERE=WHERE, execute=execute, WITH=WITH, **kwargs
        )

    def drop(self, IF_EXIST: bool = True, execute: bool = True, **kwargs):
        """
        DROP TABLE (IF EXIST)

        :param IF_EXIST: Check is table exist (boolean)
        :param execute: execute script and return db's answer (True) or return script (False)
        """

        self.db.drop(self.name, IF_EXIST=IF_EXIST, execute=execute, **kwargs)

    def find(
            self,
            WHERE: WhereType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        if not WHERE:
            WHERE = kwargs

        return self.select_all(WHERE=WHERE, ORDER_BY=ORDER_BY, LIMIT=LIMIT)


class SQLite3x:
    """
    Main SQLite3x Database Class

    :param path: Local path to database (PathType)
    :param template: template of database structure (DBTemplateType)
    """

    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        Initialization
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
        except ExecuteError:
            return False
        except Exception as error:
            logger.error(error)
            return False

    def __getitem__(self, key) -> SQLite3xTable:
        # Call method down below is necessary, otherwise it might fall in case of multiple DB objects
        self._update_constants_()

        if key not in self.tables_names:
            raise KeyError(key, "No such table in database",
                           f"Available tables: {self.tables_names}")

        return SQLite3xTable(db=self, name=key)

    def __del__(self):
        if self.connection:
            self.disconnect()

    # ============================== PRIVATE METHODS ==============================

    def _update_constants_(self):
        """
        Method to update constant vars
        """
        self.tables_names = self._get_tables_names_()
        self.tables = self._get_tables_()

    def _get_tables_(self) -> Generator[SQLite3xTable, None, None]:
        """
        Generator of table objects

        :yield: SQLite3xTable
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

    @tuples_to_lists
    def _get_tables_names_(self) -> List[str]:
        """
        Get list of tables names

        :return: None
        """

        return self.execute("SELECT name FROM sqlite_master WHERE type='table'")

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
            raise ArgumentError(args_kwargs="Unset", error="No data to execute")

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
        Parent method for all CREATE-methods
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
            raise ArgumentError(args_kwargs="Unset", error="No data to insert")

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
        Parent method for insertmany
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
            raise ArgumentError(args_kwargs="Unset", error="No data to insert")

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
            raise ArgumentError(TABLE="Argument unset and have not default value")

        if SELECT is None:
            if method != "SELECT ALL ":
                logger.warning(
                    ArgumentError(SELECT="Argument not specified, default value is '*'")
                )
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
        Parent method for DELETE method
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
        Parent method for UPDATE
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
        Parent method for drop
        """

        script += f"DROP TABLE {'IF EXISTS' if IF_EXIST else ''} {TABLE} "
        return SQLStatement(SQLRequest(script=script), self.path, self.connection)

    # ============================== PUBLIC METHODS ==============================

    def connect(self):
        """
        Create connection to database

        :return: sqlite3.connection
        """

        if not self.connection:
            self.connection = sqlite3.connect(self.path)

        # return self.connection # Not sure is this reasonable

    def disconnect(self):
        """
        Drop connection to database

        :return: None
        """

        self.connection.commit()
        self.connection.close()
        self.connection = None

    def get_table(self, name: AnyStr) -> SQLite3xTable:
        """
        Shadow method for __getitem__
        """

        return self.__getitem__(key=name)

    def execute(
            self,
            script: AnyStr = None,
            values: Tuple = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Child method of _execute_stmt_ method

        :param script: single SQLite script, might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full statement

        :return: Database answer if it has
        """

        return self._execute_stmt_(script=script, values=values, request=request)

    def executemany(
            self,
            script: AnyStr = None,
            values: Tuple = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Method to execute : param script: with :param values: if it has
        or executing :param request:

        :param script: single or multiple SQLite script(s), might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full request

        :return: Database answer if it has
        """

        return self._executemany_stmt(script=script, values=values, request=request)

    def executescript(
            self,
            script: AnyStr = None,
            request: SQLRequest = None
    ) -> Union[List, None]:
        """
        Method to execute :param script:
        or executing :param request:

        :param script: single or multiple SQLite script(s), might contains placeholders
        :param request: Instead of script and values might execute full request

        :return: Database answer if it has
        """

        return self._executescript_stmt(script=script, request=request)

    def pragma(
            self,
            *args: str,
            **kwargs
    ) -> Union[List, None]:
        """
        Set PRAGMA parameter or send PRAGMA-request

        :param args: Might be used like this:
            > db.pragma("database_list")

        :param kwargs: Might be used like this:
            > db.pragma(foreign_keys="ON")
        """

        return self._pragma_stmt_(*args, **kwargs)

    def foreign_keys(
            self,
            mode: Literal["ON", "OFF"]
    ):
        """
        Turn on/off PRAGMA parameter FOREIGN KEYS

        :param mode: "ON" or "OFF"
        """

        return self.pragma(foreign_keys=mode)

    def journal_mode(
            self,
            mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
    ):
        """
        Set PRAGMA param journal_mode

        :param mode: "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"
        """

        return self.pragma(journal_mode=mode)

    def table_info(
            self,
            table_name: str
    ):
        """
        Send PRAGMA request table_info(table_name)

        :param table_name: Name of table
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
        CREATE TABLE table-name

        Optional:
            CREATE TABLE (IF NOT EXISTS) schema-name.table-name
            (AS select-stmt) / (column-def table-constraint) (WITHOUT ROWID)

        :param name: Table name
        :param columns: Columns of table (ColumnsType)
        :param IF_NOT_EXIST: Turn on/off "IF NOT EXISTS" prefix
        :param without_rowid:
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

        :param name: Table name
        :param columns: Columns of table (ColumnsType)
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

        :param name: Table name
        :param columns: Columns of table (ColumnsType)
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
        Mark up table by template

        :param template: Structure of database (DBTemplateType)
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
    ) -> Union[Tuple, List]:
        """
        Get list of table columns

        :param table: schema-name.table-name or just table-name
        :return: List[List] of columns
        """

        columns = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")

        if not isinstance(columns, list):
            columns = [columns]

        if columns:
            return columns
        else:
            raise TableInfoError

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
        INSERT data into db's table

        :param TABLE: Table name for inserting
        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param WITH: Optional parameter.
        :param execute: execute script and return db's answer (True) or return script (False)
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
        REPLACE data into db's table

        :param TABLE: Table name for inserting
        :param WITH: Optional parameter.
        :param execute: execute script and return db's answer (True) or return script (False)
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
        INSERT many data into db's table.
        The same as regular insert but for lists of inserting values

        :param TABLE: table name for inserting
        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param execute: execute script and return db's answer (True) or return script (False)
        :param args: 1'st way set values for insert
        :param kwargs: 2'st way set values for insert
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
            TABLE: Union[str, List[str]],
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

        :param SELECT: columns to select. Value '*' by default
        :param TABLE: table for selection
        :param FROM: table for selection
        :param WHERE: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        :param WITH: with_statement
        :param JOIN: optional parameter for joining data from other tables ['groups'],
        :param ORDER_BY: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
        :param LIMIT: optional parameter for conditions, example: 10
        :param OFFSET: optional parameter for conditions, example: 5
        :param execute: execute script and return db's answer (True) or return script (False)

        :return: List[List] of selects
        """

        if not TABLE and FROM:
            TABLE = FROM

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
            TABLE: str,
            *args: str,
            SELECT: Union[List[str], str] = ALL,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            FROM: str = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:

        if not TABLE and FROM:
            TABLE = FROM

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
            TABLE: str,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            execute: bool = True,
            FROM: str = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        """
        SELECT ALL records from table

        :param TABLE: table for selection
        :param FROM: table for selection
        :param WHERE: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        :param WITH: with_statement
        :param ORDER_BY: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
        :param LIMIT: optional parameter for conditions, example: 10
        :param OFFSET: optional parameter for conditions, example: 5
        :param execute: execute script and return db's answer (True) or return script (False)

        :return: List[List] of selects
        """

        if not TABLE and FROM:
            TABLE = FROM

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

        :param TABLE: Table name as string
        :param WHERE: where_statement
        :param WITH: with_statement
        :param execute: execute script and return db's answer (True) or return script (False)
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
            WHERE: WhereType,
            OR: OrOptionsType = None,
            execute: bool = True,
            WITH: WithType = None,
            **kwargs,
    ):
        """
        UPDATE table_name SET column_name=something WHERE x=y and more complex requests

        :param TABLE: Table name
        :param SET: Column and value to set
        :param WHERE: where_statement
        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param execute: execute script and return db's answer (True) or return script (False)
        :param WITH: with_statement
        """

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
        DROP TABLE (IF EXIST) table_name

        :param TABLE: Table name
        :param IF_EXIST: Check is table exist (boolean)
        :param execute: execute script and return db's answer (True) or return script (False)
        """

        return self._drop_stmt_(
            TABLE=TABLE,
            IF_EXIST=IF_EXIST,
            execute=execute,
            **kwargs
        )


__all__ = ["SQLite3x"]
