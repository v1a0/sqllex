from sqllex.debug import logger
from sqllex.exceptions import TableInfoError
from sqllex.types.types import *
from sqllex.constants.sql import *
from sqllex.core.tools.convertors import tuple2list, return2list, crop
import sqllex.core.tools.sorters as sort
import sqllex.core.tools.parsers.parsers as parse
import sqllex.core.entities.sqlite3x.midleware as run
import sqlite3


class SQLite3xSearchCondition(str):
    def __init__(self, value: AnyStr):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

    def _str_gen(self, value, operator: str):
        if type(value) == str:
            return SQLite3xSearchCondition(
                f"({self}{operator}'{value}')"  # unsafe!
            )
        else:
            return SQLite3xSearchCondition(
                f"({self}{operator}{value})"
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

    def __or__(self, other):
        return self._str_gen(other, ' OR ')

    def __hash__(self):
        return hash(f"{self.value}")


class SQLite3xColumn:
    def __init__(self, table, name: AnyStr):
        self.table: SQLite3xTable = table
        self.name = name

    def __str__(self):
        return f"'{self.table.name}'.'{self.name}'"

    def _str_gen(self, value, operator: str):
        if type(value) == str:
            return SQLite3xSearchCondition(
                f"({self}{operator}'{value}')"  # unsafe!
            )
        else:
            return SQLite3xSearchCondition(
                f"({self}{operator}{value})"
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

    def __add__(self, value):
        return self._str_gen(value, '+')

    def __sub__(self, value):
        return self._str_gen(value, '-')

    def __mul__(self, value):
        return self._str_gen(value, '*')

    def __truediv__(self, value):
        return self._str_gen(value, '/')

    def __divmod__(self, value):
        return self._str_gen(value, '%')

    def __list__(self):
        return self.table.select_all(self.name)

    def __hash__(self):
        return hash(f"'{self.name}'.'{self.table}'")


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

    columns = list
        Generator of columns in table

    columns_names = list
        Generator of column's names in table

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

    def __str__(self):
        return self.name

    def __bool__(self):
        return bool(self.get_columns_names())

    def __getitem__(self, key) -> SQLite3xColumn:
        if key not in self.columns_names:
            raise KeyError(key, "No such column in table")

        return SQLite3xColumn(table=self, name=key)

    @property
    def columns(self) -> Generator[SQLite3xColumn, None, None]:
        for column in self.columns_names:
            yield SQLite3xColumn(table=self, name=column)

    @property
    def columns_names(self) -> List:
        return self.get_columns_names()

    def info(self):
        """
        Send PRAGMA request table_info(table_name)

        Returns
        ----------
        list
            All information about table

        """

        return self.db.pragma(f"table_info({self.name})")

    def get_columns_names(self) -> List:
        """
        Get list of table columns

        Returns
        ----------
        List[List]
            All table's columns

        """
        return self.db.get_columns_names(table=self.name)

    def insert(
            self,
            *args: InsertData,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            **kwargs: Any,
    ) -> None:
        """
        INSERT data into table

        Parameters
        ----------
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        WITH : WithType
            Optional parameter.

        Returns
        ----------
            None or SQL-script in SQLStatement
        """

        self.db.insert(
            self.name, *args, OR=OR, WITH=WITH, **kwargs
        )

    def replace(
            self,
            *args: Any,
            WITH: WithType = None,
            **kwargs: Any
    ) -> None:
        """
        REPLACE data into table

        Parameters
        ----------
        WITH : WithType
            Optional parameter.

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        self.db.replace(self.name, *args, **kwargs, WITH=WITH)

    def insertmany(
            self,
            *args: Union[List[InsertData], Tuple[InsertData]],
            OR: OrOptionsType = None,
            **kwargs: Any,
    ) -> None:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        Parameters
        ----------
        args : Union[List, Tuple]
            1'st way set values for insert
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        self.db.insertmany(self.name, *args, OR=OR, **kwargs)

    def select(
            self,
            SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
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

        Returns
        ----------
        List[List]
            selected data

        """

        return self.db.select(
            self.name,
            SELECT=SELECT,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def select_distinct(
            self,
            SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        return self.db.select_distinct(
            self.name,
            SELECT=SELECT,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def select_all(
            self,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
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

        Returns
        ----------
        List[List]
            selected data

        """

        return self.db.select_all(
            self.name,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def delete(
            self,
            WHERE: WhereType = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
        """
        DELETE FROM table WHERE {something}

        Parameters
        ----------
        WHERE : WhereType
            optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        WITH : WithType
            with_statement (don't really work well)

        """

        self.db.delete(
            self.name, WHERE=WHERE, WITH=WITH, **kwargs
        )

    def update(
            self,
            SET: Union[List, Tuple, Mapping],
            WHERE: WhereType = None,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
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
        WITH : WithType
            with_statement (don't really work well)
        """

        self.db.update(
            self.name, SET=SET, OR=OR, WHERE=WHERE, WITH=WITH, **kwargs
        )

    def updatemany(
            self,
            SET: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple]] = None,
            **kwargs,
    ) -> None:
        """
        ACTUALLY IT'S JUST "INSERT OR REPLACE" BUT SOUNDS EASIER TO UNDERSTAND

        Update many values (or insert)

        Parameters
        ----------
        SET : Union[List, Tuple, Mapping]
            Values to insert or update
        """

        self.db.updatemany(TABLE=self.name, SET=SET, **kwargs)

    def drop(self, IF_EXIST: bool = True, **kwargs):
        """
        DROP TABLE (IF EXIST)

        Parameters
        ----------
        IF_EXIST : bool
            Check is table exist (boolean)
        """

        self.db.drop(self.name, IF_EXIST=IF_EXIST, **kwargs)

    def find(
            self,
            WHERE: WhereType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            **kwargs,
    ) -> Union[SQLRequest, List]:
        """
        Find all records in table where_

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
    __connection : Union[sqlite3.Connection, None]
        SQLite connection
    __path : PathType
        Local __str__ to database (PathType)

    """

    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        Initialization

        Parameters
        ----------
        path : PathType
            Local __str__ to database (PathType)
        template : DBTemplateType
            template of database structure (DBTemplateType)

        """
        self.__connection: Union[sqlite3.Connection, None] = None
        self.__path = path
        self.journal_mode(mode="WAL")  # make db little bit faster
        self.foreign_keys(mode="ON")
        if template:
            self.markup(template=template)

    @property
    def connection(self):
        return self.__connection

    @property
    def path(self):
        return self.__path

    @property
    def tables(self):
        return self._get_tables()

    @property
    def tables_names(self):
        return self._get_tables_names()

    def __str__(self):
        return f"{{SQLite3x: __str__='{self.path}'}}"

    def __bool__(self):
        try:
            return bool(self.pragma("database_list"))
        except Exception as error:
            logger.error(error)
            return False

    def __getitem__(self, key) -> SQLite3xTable:
        # To call method down below is necessary,
        # otherwise it might fall in case of multiple DB objects

        if key not in self.tables_names:
            raise KeyError(key, "No such table in database",
                           f"Available tables: {self.tables_names}")

        return SQLite3xTable(db=self, name=key)

    def __del__(self):
        if self.connection:
            self.disconnect()

    # ============================== PRIVATE METHODS ==============================

    def _get_tables(self) -> Generator[SQLite3xTable, None, None]:
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

    def _get_tables_names(self) -> List[str]:
        """
        Get list of tables names from database

        Returns
        ----------
        List[str]
            list of tables names

        """
        return tuple2list(
            self.execute("SELECT name FROM sqlite_master WHERE type='table'"),
            remove_one_len=True
        )

    @return2list
    @run.execute
    def _execute_stmt(
            self, script: AnyStr = None, values: Tuple = None, request: SQLRequest = None
    ):
        """
        Parent method for execute
        """

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path, self.connection)
        else:
            return SQLStatement(request, self.path, self.connection)

    @return2list
    @run.executemany
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

    @return2list
    @run.executescript
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

    @return2list
    @run.execute
    def _pragma_stmt(self, *args: str, **kwargs):
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

    @run.execute
    def _create_stmt(
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
                params = sorted(params, key=lambda par: sort.column_types(par))
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

    @run.execute
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @parse.args_parser
    def _insert_stmt(
            self, *args: Any, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for INSERT-like methods

        INSERT INTO request (aka insert-stmt) and REPLACE INTO request

        """

        # parsing args or kwargs for _columns and insert_values
        if args:
            _columns = self.get_columns_names(table=TABLE)
            _columns, args = crop(_columns, args)
            insert_values = args

        elif kwargs:
            _columns = tuple(kwargs.keys())
            insert_values = list(kwargs.values())

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        script += (
            f"{' ' if script else ''}"
            f"INTO '{TABLE}' ("
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

    @run.execute
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @parse.args_parser
    def _fast_insert_stmt(
            self, *args, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for fast INSERT-like methods

        'INSERT INTO' request and 'REPLACE INTO' request without columns names
        (without get_columns_names req because it's f-g slow)
        """

        if not args:
            raise sqlite3.OperationalError

        script += (
            f"{' ' if script else ''}"
            f"INTO '{TABLE}' "
            f"VALUES ("
            f"{', '.join('?' * len(args))}) "
        )

        values = tuple(list(values) + list(args))

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @logger.catch
    @run.executemany
    @parse.or_param_
    @parse.from_as_
    @parse.args_parser
    def _insertmany_stmt(
            self,
            TABLE: AnyStr,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            script="",
            values=(),
            **kwargs: Any,
    ):
        """
        Parent method for insertmany method

        Comment:
            args also support numpy.array value

        """

        if args:
            args = list(filter(lambda ar: len(ar) > 0, args[0]))  # removing [] (empty lists from inserting values)

            if len(args) == 0:  # if args empty after filtering, break the function, yes it'll break
                logger.warning("insertmany/updatemany failed, due to no values to insert/update")
                return

            values = list(
                map(lambda arg: list(arg), args)
            )

            max_l = max(map(lambda arg: len(arg), values))  # max len of arg in values
            temp_ = [0 for _ in range(max_l)]  # example values [] for script
            stmt = self._insert_stmt(temp_, script=script, TABLE=TABLE,
                                     execute=False)  # getting stmt for maxsize value
            max_len = len(stmt.request.values)  # len of max supported val list

            for i in range(len(values)):  # cropping or appending values, making it's needed size
                len_val_i = len(values[i])
                if len_val_i < max_len:
                    values[i] += [None] * (max_len - len_val_i)
                elif len_val_i > max_len:
                    values[i] = values[i][:max_len]

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

            stmt = self._insert_stmt(temp_, script=script, TABLE=TABLE,
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

    @return2list
    @run.execute
    @parse.offset_
    @parse.limit_
    @parse.order_by_
    @parse.where_
    @parse.join_
    @parse.with_
    @parse.from_as_
    def _select_stmt(
            self,
            TABLE: Union[str, SQLite3xTable],
            script="",
            values=(),
            method: AnyStr = "SELECT ",
            SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]]] = None,
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

        script += f"{method} " f"{', '.join(str(sel) for sel in SELECT)} " f"FROM '{str(TABLE)}' "

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @run.execute
    @parse.where_
    @parse.with_
    def _delete_stmt(self, TABLE: str, script="", values=()):
        """
        Parent method for delete method

        """

        script += f"DELETE FROM '{TABLE}' "
        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @run.execute
    @parse.where_
    @parse.or_param_
    @parse.with_
    def _update_stmt(
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

        script += f"UPDATE '{TABLE}' SET "

        for (key, val) in set_.items():
            if issubclass(type(key), SQLite3xColumn):
                script += f"'{key.name}'="
            else:
                script += f"'{key}'="

            if issubclass(type(val), SQLite3xSearchCondition):
                script += f"{val}, "
            else:
                script += "?, "
                values = tuple(list(values) + [val])


        script = script[:-2]

        return SQLStatement(
            SQLRequest(script=script, values=values), self.path, self.connection
        )

    @run.execute
    def _drop_stmt(
            self,
            TABLE: AnyStr,
            IF_EXIST: bool = True,
            script="",
            **kwargs
    ):
        """
        Parent method for drop method

        """

        script += f"DROP TABLE {'IF EXISTS' if IF_EXIST else ''} '{TABLE}' "
        return SQLStatement(SQLRequest(script=script), self.path, self.connection)

    # ============================== PUBLIC METHODS ==============================

    def connect(self):
        """
        Create connection to database

        Creating sqlite3.connect(__str__) connection to interact with database

        """

        if not self.connection:
            self.__connection = sqlite3.connect(self.path)

        # Not sure is this reasonable
        # return self.connection

    def disconnect(self):
        """
        Drop connection to database

        Commit changes and close connection

        """

        self.connection.commit()
        self.connection.close()
        self.__connection = None

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

        return self._execute_stmt(script=script, values=values, request=request)

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

        return self._pragma_stmt(*args, **kwargs)

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

        self._create_stmt(
            temp="",
            name=name,
            columns=columns,
            IF_NOT_EXIST=IF_NOT_EXIST,
            without_rowid=without_rowid,
        )

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

        self._create_stmt(
            temp="TEMP",
            name=name,
            columns=columns,
            **kwargs
        )

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

        self._create_stmt(
            temp="TEMPORARY",
            name=name,
            columns=columns,
            **kwargs
        )

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

        for column in columns:
            yield SQLite3xColumn(table=self, name=column)

    def get_columns_names(
            self,
            table: AnyStr
    ) -> List[str]:
        """
        Get list of names of table columns

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
            **kwargs: Any,
    ) -> None:
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

        Returns
        ----------
            None or SQL-script in SQLStatement
        """

        try:
            if args:
                self._fast_insert_stmt(
                    *args,
                    script="INSERT",
                    OR=OR,
                    TABLE=TABLE,
                    **kwargs,
                    WITH=WITH,
                )

            else:
                raise ValueError

        except (sqlite3.OperationalError, ValueError):
            self._insert_stmt(
                *args,
                script="INSERT",
                OR=OR,
                TABLE=TABLE,
                **kwargs,
                WITH=WITH,
            )

    def replace(
            self,
            TABLE: AnyStr,
            *args: Any,
            WITH: WithType = None,
            **kwargs: Any,
    ) -> None:
        """
        REPLACE data into table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        WITH : WithType
            Optional parameter.

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        try:
            if args:
                self._fast_insert_stmt(
                    *args,
                    script="REPLACE",
                    TABLE=TABLE,
                    **kwargs,
                    WITH=WITH,
                )
            else:
                raise ValueError

        except (sqlite3.OperationalError, ValueError):
            self._insert_stmt(
                *args,
                script="REPLACE",
                TABLE=TABLE,
                **kwargs,
                WITH=WITH
            )

    def insertmany(
            self,
            TABLE: AnyStr,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            OR: OrOptionsType = None,
            **kwargs: Any,
    ) -> None:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        args : Union[List, Tuple]
            1'st way set values for insert
            P.S: args also support numpy.array value
        OR : OrOptionsType
            Optional parameter. If INSERT failed, type OrOptionsType
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """
        if len(args) > 1:
            args = [args]

        self._insertmany_stmt(
            TABLE,
            *args,
            OR=OR,
            script="INSERT",
            values=(),
            **kwargs
        )

    def select(
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
            _method="SELECT",
            **kwargs,
    ) -> Union[SQLStatement, List[Any]]:
        """
        SELECT data from table

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
        _method: str
            DON'T CHANGE IT! special argument for unite select_all, select_distinct into select()

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

        if SELECT is None:
            SELECT = ALL

        if not WHERE:
            WHERE = kwargs
            kwargs = {}

        return self._select_stmt(
            SELECT=SELECT,
            TABLE=TABLE,
            method=_method,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            **kwargs,
        )

    def select_distinct(
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
        SELECT distinct from table

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

        return self.select(
            TABLE=TABLE,
            _method="SELECT DISTINCT ",
            SELECT=SELECT,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            FROM=FROM,
            JOIN=JOIN,
            **kwargs
        )

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

        return self.select(
            TABLE=TABLE,
            _method="SELECT ALL ",
            SELECT=SELECT,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            FROM=FROM,
            JOIN=JOIN,
            **kwargs
        )

    def delete(
            self,
            TABLE: str,
            WHERE: WhereType = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
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

        """

        if not WHERE:
            WHERE = kwargs

        self._delete_stmt(
            TABLE=TABLE,
            WHERE=WHERE,
            WITH=WITH,
        )

    def update(
            self,
            TABLE: AnyStr,
            SET: Union[List, Tuple, Mapping],
            WHERE: WhereType = None,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
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
        WITH : WithType
            with_statement (don't really work well)
        """

        if not WHERE:
            WHERE = kwargs

        self._update_stmt(
            TABLE=TABLE,
            SET=SET,
            OR=OR,
            WHERE=WHERE,
            WITH=WITH,
            **kwargs,
        )

    def updatemany(
            self,
            TABLE: AnyStr,
            SET: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple]] = None,
            **kwargs,
    ) -> None:
        """
        ACTUALLY IT'S JUST "INSERT OR REPLACE" BUT SOUNDS EASIER TO UNDERSTAND

        Update (or insert) many values

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        SET : Union[List, Tuple, Mapping]
            Values to insert or update
            P.S: SET also support numpy.array value
        """

        if SET is not None:
            self._insertmany_stmt(
                TABLE,
                SET,
                script="INSERT",
                OR=REPLACE,
                **kwargs,
            )

        else:
            # In case if SET == []
            logger.warning(
                f"SQLite3x.updatemany "
                f"got empty list of data to update or got nothing at all, "
                f"SET={SET}"
            )

    def drop(
            self,
            TABLE: AnyStr,
            IF_EXIST: bool = True,
            **kwargs
    ) -> None:
        """
        DROP TABLE (IF EXIST)

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        IF_EXIST : bool
            Check is table exist (boolean)
        """

        self._drop_stmt(
            TABLE=TABLE,
            IF_EXIST=IF_EXIST,
            **kwargs
        )


__all__ = [
    "SQLite3x",  # lgtm [py/undefined-export]
    "SQLite3xTable",  # lgtm [py/undefined-export]
    "SQLite3xColumn",  # lgtm [py/undefined-export]
    "SQLite3xSearchCondition"  # lgtm [py/undefined-export]
]
