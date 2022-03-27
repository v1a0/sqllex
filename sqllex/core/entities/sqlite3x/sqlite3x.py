"""
PostgreSQLxTable and PostgreSQLx
"""
from sqllex.core.entities.abc import \
    AbstractDatabase as ABDatabase, \
    AbstractTable as ABTable, \
    AbstractColumn as ABColumn, \
    AbstractTransaction
import sqllex.core.tools.parsers.parsers as parse
from sqllex.debug import logger
from sqllex.exceptions import TableNotExist
from sqllex.types.types import *
import sqllex.core.entities.sqlite3x.middleware as middleware
import sqlite3
from sqllex.core.tools.docs_helpers import copy_docs
import sqllex.core.entities.sqlite3x.script_gens as script_gen


class SQLite3xTransaction(AbstractTransaction):
    @property
    def __name__(self):
        return "SQLite3xTransaction"


class SQLite3xTable(ABTable):
    """
    Sub-class of SQLite3x, itself one table of ABTable
    Have same methods but without table name argument

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

        #        __slots__ = ('__path', '__connection') # Memory optimisation !!!

        super(SQLite3xTable, self).__init__(db=db, name=name)

        if not isinstance(db, SQLite3x):
            raise TypeError(f"Argument db have oto be SQLite3x not {type(db)}")

        self.db: SQLite3x = db
        self.name: AnyStr = name

    @copy_docs(ABTable.__getitem__)
    def __getitem__(self, key) -> ABColumn:
        if key not in self.columns_names:
            raise KeyError(key, "No such column in table")

        return ABColumn(table=self.name, name=key, placeholder=self.db.placeholder)

    @property
    @copy_docs(ABTable.columns)
    def columns(self) -> Generator[ABColumn, None, None]:
        for column in self.columns_names:
            yield ABColumn(table=self.name, name=column, placeholder=self.db.placeholder)

    @property
    @copy_docs(ABTable.columns_names)
    def columns_names(self) -> Tuple:
        return self.get_columns_names()

    # ============================ ADDITIONAL PUBLIC METHODS ===========================

    def info(self):
        """
        Send PRAGMA request table_info(table_name)

        Returns
        ----------
        list
            All information about table

        """

        return self.db.pragma(f"table_info({self.name})")


class SQLite3x(ABDatabase):
    """
    Main class to interact with SQLite3 databases.
    It's parent class for SQLite3xTable.

    (based on AbstractDatabase)
    """

    # ============================ MAGIC METHODS =================================

    def __init__(
            self,
            path: PathType = "sql3x.db",
            template: DBTemplateType = None,
            init_connection=True,
            connection: sqlite3.Connection = None,
            **connection_kwargs
    ):
        """
        Initialization

        Parameters
        ----------
        path : PathType
            Local __str__ to database (PathType)
        template : DBTemplateType
            template of database structure (DBTemplateType)
        init_connection : bool
            Create connection to database with database class object initialisation
        connection: sqlite3.Connection
            Already existing connection to database
        connection_kwargs: Any
            Optional parameters for creating connection with db (for example: check_same_thread=False)
        """

        #        __slots__ = ('__path', '__connection') # Memory optimisation !!!

        super(SQLite3x, self).__init__(placeholder='?')

        # path
        if not path:
            raise ValueError("Path can't be empty or undefined")
        else:
            self.__path = path

        # connection
        self.__connection = connection  # init connection

        if init_connection and connection_kwargs and self.connection:
            # if connection already exist but func also got an connection_kwargs
            logger.warning(f"Connection already exists, parameters ({connection_kwargs}) have not been set")

        if init_connection and not self.connection:
            self.connect(path=self.path, **connection_kwargs)  # creating connection with db

        # mark_up
        if template:
            self.markup(template=template)

    @copy_docs(ABDatabase.__str__)
    def __str__(self):
        return f"{{SQLite3x: '{self.path}'}}"

    @copy_docs(ABDatabase.__bool__)
    def __bool__(self):
        try:
            return bool(self.connection)
        except Exception as error:
            logger.error(error)
            return False

    # =============================== PROPERTIES ==================================

    @copy_docs(ABDatabase.transaction)
    @property
    def transaction(self) -> SQLite3xTransaction:
        return SQLite3xTransaction(db=self)

    @copy_docs(ABDatabase.connection)
    @property
    def connection(self) -> Union[sqlite3.Connection, None]:
        try:
            return self.__connection
        except AttributeError:
            # TODO: I have no idea why but some tests falling with exception
            # AttributeError: 'SQLite3x' object has no attribute '_SQLite3x__connection'
            logger.debug("WTF??? self.__connection undef. ???")

            return None

    @property
    def path(self) -> PathType:
        """
        Path to your local sqlite database
        """
        return self.__path

    # ================================== STMT'S ====================================

    @copy_docs(ABDatabase._create_stmt)
    def _create_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._create_stmt(*args, **kwargs)

    @parse.where_(placeholder='?')
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._insert_stmt)
    def _insert_stmt(self, *args, **kwargs: Any) -> ScriptAndValues:
        return super(SQLite3x, self)._insert_stmt(*args, **kwargs)

    @parse.where_(placeholder='?')
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._fast_insert_stmt)
    def _fast_insert_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._fast_insert_stmt(*args, **kwargs)

    @parse.where_(placeholder='?')
    @parse.or_param_
    @parse.from_as_
    @copy_docs(ABDatabase._insertmany_stmt)
    def _insertmany_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._insertmany_stmt(*args, **kwargs)

    @parse.offset_
    @parse.limit_
    @parse.order_by_
    @parse.group_by_
    @parse.where_(placeholder='?')
    @parse.join_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._select_stmt)
    def _select_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._select_stmt(*args, **kwargs)

    @parse.where_(placeholder='?')
    @parse.with_
    @copy_docs(ABDatabase._delete_stmt)
    def _delete_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._delete_stmt(*args, **kwargs)

    @parse.where_(placeholder='?')
    @parse.or_param_
    @parse.with_
    @copy_docs(ABDatabase._update_stmt)
    def _update_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(SQLite3x, self)._update_stmt(*args, **kwargs)

    # ========================= ADDITIONAL STMT'S ====================================

    @staticmethod
    def _pragma_stmt(*args: str, **kwargs):
        """
        Constructor of pragma statements
        """

        if args:
            parameter = args[0]
            script = script_gen.pragma_args(parameter)
        elif kwargs:
            parameter, value = tuple(kwargs.items())[0]
            script = script_gen.pragma_kwargs(parameter=parameter, value=value)
        else:
            raise ValueError(f"No data to execute, args: {args}, kwargs: {kwargs}")

        return script

    # ============================= ABC PRIVATE METHODS ============================

    @copy_docs(ABDatabase._executor)
    def _executor(self, script: AnyStr, values: Tuple = None, spec: Number = 0):
        if spec == 1:
            return middleware.execute(script=script, values=values, connection=self.connection, path=self.path)
        elif spec == 2:
            return middleware.executemany(script=script, values=values, connection=self.connection, path=self.path)
        elif spec == 3:
            return middleware.executescript(script=script, connection=self.connection, path=self.path)

    @copy_docs(ABDatabase._get_table)
    def _get_table(self, name) -> SQLite3xTable:
        return SQLite3xTable(db=self, name=name)

    @copy_docs(ABDatabase._get_tables)
    def _get_tables(self) -> Generator[SQLite3xTable, None, None]:
        for tab_name in self.tables_names:
            yield self._get_table(tab_name)

    @copy_docs(ABDatabase._get_tables_names)
    def _get_tables_names(self) -> Tuple:
        return tuple(map(lambda ret: ret[0], self.execute("SELECT name FROM sqlite_master WHERE type='table'")))

    # ============================== ABC PUBLIC METHODS ============================

    @copy_docs(ABDatabase.connect)
    def connect(
            self,
            path=None,
            **kwargs
    ) -> sqlite3.Connection:
        """
        Creating sqlite3.connect() connection to interact with database

        Optional parameters (default):
            path=self.path

        Additional kwargs for sqlite3.connect()
            path=None,
            timeout=None,
            detect_types=None,
            isolation_level=None,
            check_same_thread=None,
            factory=None,
            cached_statements=None,
            uri=None,
        """
        if path is None:
            path = self.path
        else:
            self.__path = path  # Not sure about this

        if not self.connection:
            self.__connection = sqlite3.connect(path, **kwargs)
            self.journal_mode(mode="WAL")  # make db little bit faster
            self.foreign_keys(mode="ON")   # turning on foreign keys
            return self.connection

        else:
            logger.warning("Connection already exist")

    @copy_docs(ABDatabase.disconnect)
    def disconnect(self):
        if not self.connection:
            return

        self.connection.commit()
        self.connection.close()
        self.__connection = None

    @copy_docs(ABDatabase.get_columns_names)
    def get_columns_names(
            self,
            table: AnyStr
    ) -> Tuple:

        try:
            columns_: Tuple[Tuple] = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")
            columns: Tuple = tuple(map(lambda item: item[0], columns_))

        except sqlite3.OperationalError:
            # Fix for compatibility issues #19, by some reason it can't find PRAGMA_TABLE_INFO table
            columns_: Tuple[Tuple] = self.pragma(f"table_info('{table}')")
            columns: Tuple = tuple(map(lambda item: item[1], columns_))

        if not columns:
            raise TableNotExist(f"No columns or table {table}")

        return columns

    # ========================== ADDITIONAL PUBLIC METHODS =========================

    def pragma(
            self,
            *args: str,
            **kwargs: NumStr
    ) -> Union[Tuple, None]:
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
        Union[Tuple, None]
            ABDatabase answer if it has

        """

        script = self._pragma_stmt(*args, **kwargs)
        return self.execute(script=script)

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

        Parameters
        ----------
        table_name : str
            Name of table

        """

        return self.pragma(f"table_info({table_name})")


__all__ = [
    "SQLite3x",  # lgtm [py/undefined-export]
    "SQLite3xTable",  # lgtm [py/undefined-export]
    "SQLite3xTransaction",  # lgtm [py/undefined-export]
]
