from sqllex.core.entities.abc import AbstractDatabase, AbstractTable, AbstractColumn, AbstractSearchCondition
from sqllex.debug import logger
from sqllex.exceptions import TableInfoError
from sqllex.types.types import *
from sqllex.core.tools.convertors import tuple2list, return2list
import sqllex.core.entities.sqlite3x.middleware as middleware
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

        super(SQLite3x, self).__init__()

        self.__path = path
        self.__connection = None       # init connection (?)
        self.connect()                 # creating connection with db
        self.journal_mode(mode="WAL")  # make db little bit faster
        self.foreign_keys(mode="ON")   # turning on foreign keys

        if template:
            self.markup(template=template)

    def __str__(self):
        return f"{{SQLite3x: '{self.path}'}}"

    def __bool__(self):
        try:
            return bool(self.pragma("database_list"))
        except Exception as error:
            logger.error(error)
            return False

    # ========================== ABC METHODS INIT =================================
    def _executor(self, script: AnyStr, values: Tuple = None, spec: Number = 0):
        """
        Execute scripts with values

        Parameters
        ----------
        spec : Number
            Id of execution case:
                1. Regular Sqlite3.execute
                2. Sqlite3.executemany
                3. Sqlite3.executescript
        """
        if spec == 1:
            return middleware.execute(script=script, values=values, connection=self.connection, path=self.path)
        elif spec == 2:
            return middleware.executemany(script=script, values=values, connection=self.connection, path=self.path)
        elif spec == 3:
            return middleware.executescript(script=script, connection=self.connection, path=self.path)

    # =============================== PROPERTIES ==================================

    @property
    def connection(self) -> Union[sqlite3.Connection, None]:
        return self.__connection

    @property
    def path(self) -> PathType:
        return self.__path

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
