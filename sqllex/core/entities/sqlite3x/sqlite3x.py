from sqllex.core.entities.abc import AbstractDatabase, AbstractTable, AbstractColumn, AbstractSearchCondition
from sqllex.debug import logger
from sqllex.exceptions import TableInfoError
from sqllex.types.types import *
from sqllex.core.tools.convertors import tuple2list, return2list
import sqllex.core.entities.sqlite3x.midleware as run
import sqlite3


class SQLite3xSearchCondition(AbstractSearchCondition):
    def _str_gen(self, value, operator: str):
        if type(value) == str:
            return SQLite3xSearchCondition(
                f"({self}{operator}'{value}')"  # unsafe!
            )
        else:
            return SQLite3xSearchCondition(
                f"({self}{operator}{value})"
            )


class SQLite3xColumn(AbstractColumn):
    """
    Sub-class of SQLite3xTable, itself one column of table (SQLite3xTable)
    Have same methods but without table name argument
    Attributes
    ----------
    table : SQLite3xTable
        SQLite3xTable parent table object
    name : str
        Name of column

    Existing for generating SQLite3xSearchCondition for WHERE, SET
    and other parameters of parents classes

    db['table_name']['column_name'] = x
    db['table_name']['column_name'] > x
    db['table_name']['column_name'] >= x
    db['table_name']['column_name'] != x
    ...
    db['table_name']['column_name'] / x
    """

    def _str_gen(self, value, operator: str):
        if type(value) == str:
            return SQLite3xSearchCondition(
                f"({self}{operator}'{value}')"  # unsafe!
            )
        else:
            return SQLite3xSearchCondition(
                f"({self}{operator}{value})"
            )

    def __lt__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '<')

    def __le__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '<=')

    def __eq__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '=')

    def __ne__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '<>')

    def __gt__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '>')

    def __ge__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '>=')

    def __add__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '+')

    def __sub__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '-')

    def __mul__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '*')

    def __truediv__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '/')

    def __divmod__(self, value) -> SQLite3xSearchCondition:
        return self._str_gen(value, '%')

    def __hash__(self):
        return super(SQLite3xColumn, self).__hash__()


class SQLite3xTable(AbstractTable):
    """
    Sub-class of SQLite3x, itself one table of Database
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

        super(SQLite3xTable, self).__init__(db=db, name=name)

        if not isinstance(db, SQLite3x):
            raise TypeError(f"Argument db have oto be SQLite3x not {type(db)}")
        self.db: SQLite3x = db
        self.name: AnyStr = name

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


class SQLite3x(AbstractDatabase):
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

        super().__init__()      # self.__connection = None

        self.__path = path
        self.__connection = None
        self.connect()

        self.journal_mode(mode="WAL")  # make db little bit faster
        self.foreign_keys(mode="ON")   # turning on foreign keys

        if template:
            self.markup(template=template)

    @property
    def path(self) -> PathType:
        return self.__path

    @property
    def connection(self) -> Union[sqlite3.Connection, None]:
        return self.__connection

    def __str__(self):
        return f"{{SQLite3x: '{self.path}'}}"

    def __bool__(self):
        try:
            return bool(self.pragma("database_list"))
        except Exception as error:
            logger.error(error)
            return False

    # ============================== PRIVATE METHODS ==============================

    def _get_table(self, name) -> SQLite3xTable:
        super(SQLite3x, self)._get_table(name=name)
        return SQLite3xTable(db=self, name=name)

    def _get_tables(self) -> Generator[SQLite3xTable, None, None]:
        """
        Generator of tables as SQLite3xTable objects

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
            yield self._get_table(tab_name)

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

        script = super(SQLite3x, self)._pragma_stmt(*args, **kwargs)
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

        script, values = super(SQLite3x, self)._create_stmt(
            temp=temp,
            name=name,
            columns=columns,
            IF_NOT_EXIST=IF_NOT_EXIST,
            without_rowid=without_rowid
        )

        return SQLStatement(
            SQLRequest(script=script, values=values), self.path, self.connection
        )

    @run.execute
    def _insert_stmt(
            self, *args: Any, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for INSERT-like methods

        INSERT INTO request (aka insert-stmt) and REPLACE INTO request

        """

        script, values = super(SQLite3x, self)._insert_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs,
        )

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)


    @run.execute
    def _fast_insert_stmt(
            self, *args, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ):
        """
        Parent method for fast INSERT-like methods

        'INSERT INTO' request and 'REPLACE INTO' request without columns names
        (without get_columns_names req because it's f-g slow)
        """

        script, values = super(SQLite3x, self)._fast_insert_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs,
        )

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @run.executemany
    def _insertmany_stmt(
            self,
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple],
            TABLE: AnyStr,
            script="",
            values=(),
            **kwargs: Any,
    ):
        """
        Parent method for insertmany method

        Comment:
            args also support numpy.array value

        """

        script, values = super(SQLite3x, self)._insertmany_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs,
        )

        return SQLStatement(
            SQLRequest(script, values), self.path, self.connection
        )

    @return2list
    @run.execute
    def _select_stmt(
            self,
            TABLE: Union[str, SQLite3xTable],
            script="",
            values=(),
            method: AnyStr = "SELECT ",
            SELECT: Union[str, SQLite3xColumn, List[Union[str, SQLite3xColumn]], Tuple[Union[str, SQLite3xColumn]]] = None,
            **kwargs,
    ):
        """
        Parent method for all SELECT-like methods

        """

        script, values = super(SQLite3x, self)._select_stmt(
            TABLE,
            script=script,
            values=values,
            method=method,
            SELECT=SELECT,
            **kwargs,
        )

        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @run.execute
    def _delete_stmt(self, TABLE: str, script="", values=(), **kwargs):
        """
        Parent method for delete method

        """

        script, values = super(SQLite3x, self)._delete_stmt(
            TABLE=TABLE,
            script=script,
            values=values
        )
        return SQLStatement(SQLRequest(script, values), self.path, self.connection)

    @run.execute
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

        script, values = super(SQLite3x, self)._update_stmt(
            TABLE=TABLE,
            SET=SET,
            script=script,
            values=values,
            **kwargs
        )

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

        script = super(SQLite3x, self)._drop_stmt(
            TABLE=TABLE,
            IF_EXIST=IF_EXIST,
            script=script,
            **kwargs,
        )

        return SQLStatement(SQLRequest(script=script), self.path, self.connection)

    # ============================== PUBLIC METHODS ==============================

    def connect(self):
        """
        Create connection to database

        Creating sqlite3.connect(__str__) connection to interact with database

        """

        if not self.connection:
            self.__connection = sqlite3.connect(self.path)

        else:
            logger.warning("Connection already exist")

        # Not sure is this reasonable
        # return self.connection

    def disconnect(self):
        """
        Drop connection to database

        Commit changes and close connection

        """

        if not self.connection:
            return

        self.connection.commit()
        self.connection.close()
        self.__connection = None

    def add_column(
            self,
            table: AnyStr,
            column: ColumnsType
    ) -> None:
        """
        Adds column to the table

        Parameters
        ----------
        table : AnyStr
            Name of table
        column : ColumnDataType
            Columns of table (ColumnsType-like)
            Column name and SQL type e.g. {'value': INTEGER}

        Returns
        ----------
        None
        """

        for (column_name, column_type) in column.items():
            if not isinstance(column_type, (list, tuple)):
                column_type = [column_type]

            self.execute(
                f"ALTER TABLE "
                f"'{table}' "
                f"ADD "
                f"'{column_name}' "
                f"{' '.join(ct for ct in column_type)}")

    def remove_column(
            self,
            table: AnyStr,
            column: Union[AnyStr, SQLite3xColumn]
    ):
        """
        Removes column from the table

        Parameters
        ----------
        table : AnyStr
            Name of table
        column : Union[AnyStr, SQLite3xColumn]
            Name of column or SQLite3xColumn object.

        Returns
        ----------
        None
        """

        column_name = column

        if isinstance(column, SQLite3xColumn):
            column_name = column.name

        self.execute(
            f"ALTER TABLE '{table}' DROP COLUMN '{column_name}'")

    def get_table(
            self,
            name: AnyStr
    ) -> SQLite3xTable:
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

        return self._get_table(name=name)


    def get_columns(
            self,
            table: AnyStr
    ) -> Generator[SQLite3xColumn, None, None]:
        """
        Get list of table columns like an SQLite3xColumn objects

        Parameters
        ----------
        table : AnyStr
            Name of table

        Returns
        ----------
        Generator[SQLite3xColumn]
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
        Get list of names of table columns as strings

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


__all__ = [
    "SQLite3x",  # lgtm [py/undefined-export]
    "SQLite3xTable",  # lgtm [py/undefined-export]
    "SQLite3xColumn",  # lgtm [py/undefined-export]
    "SQLite3xSearchCondition"  # lgtm [py/undefined-export]
]
