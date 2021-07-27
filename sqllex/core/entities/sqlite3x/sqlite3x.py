from sqllex.core.entities.abc import AbstractDatabase, AbstractTable, AbstractColumn
from sqllex.debug import logger
from sqllex.exceptions import TableInfoError
from sqllex.types.types import *
from sqllex.core.tools.convertors import tuple2list, return2list
import sqllex.core.entities.sqlite3x.middleware as middleware
import sqlite3


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

    def __getitem__(self, key) -> AbstractColumn:
        if key not in self.columns_names:
            raise KeyError(key, "No such column in table")

        return AbstractColumn(table=self.name, name=key)

    @property
    def columns(self) -> Generator[AbstractColumn, None, None]:
        for column in self.columns_names:
            yield AbstractColumn(table=self.name, name=column)

    @property
    def columns_names(self) -> Tuple:
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

        super(SQLite3x, self).__init__(placeholder='?')

        self.__path = path
        self.__connection = None       # init connection
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

    def _get_tables_names(self) -> Tuple[str]:
        """
        Get list of tables names from database

        Returns
        ----------
        List[str]
            list of tables names

        """
        return tuple(map(lambda ret: ret[0], self.execute("SELECT name FROM sqlite_master WHERE type='table'")))

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



    def get_columns_names(
            self,
            table: AnyStr
    ) -> Tuple[str]:
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
            columns_: Tuple[Tuple[str]] = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")
            columns: Tuple = tuple(map(lambda item: item[0], columns_))

        except sqlite3.OperationalError:
            # Fix for compatibility issues #19, by some reason it can't find PRAGMA_TABLE_INFO table
            columns_: Tuple[Tuple[str]] = self.pragma(f"table_info('{table}')")
            columns: Tuple = tuple(map(lambda item: item[1], columns_))

        if not columns:
            raise TableInfoError

        return columns


__all__ = [
    "SQLite3x",  # lgtm [py/undefined-export]
    "SQLite3xTable",  # lgtm [py/undefined-export]
]
