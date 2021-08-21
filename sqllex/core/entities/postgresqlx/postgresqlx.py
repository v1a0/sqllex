from sqllex.core.entities.abc import AbstractDatabase, AbstractTable, AbstractColumn
import sqllex.core.tools.parsers.parsers as parse
from sqllex.debug import logger
from sqllex.exceptions import TableInfoError
from sqllex.types.types import *
import sqllex.core.entities.postgresqlx.middleware as middleware
import psycopg2
from psycopg2.extensions import connection

class PostgreSQLxTable(AbstractTable):
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

#        __slots__ = ('__path', '__connection') # Memory optimisation !!!

        super(PostgreSQLxTable, self).__init__(db=db, name=name)

        if not isinstance(db, PostgreSQLx):
            raise TypeError(f"Argument db have oto be SQLite3x not {type(db)}")
        self.db: PostgreSQLx = db
        self.name: AnyStr = name

    def __getitem__(self, key) -> AbstractColumn:
        if key not in self.columns_names:
            raise KeyError(key, "No such column in table")

        return AbstractColumn(table=self.name, name=key, placeholder='%s')

    @property
    def columns(self) -> Generator[AbstractColumn, None, None]:
        for column in self.columns_names:
            yield AbstractColumn(table=self.name, name=column, placeholder='%s')

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


class PostgreSQLx(AbstractDatabase):
    """
    Main SQLite3x Database Class

    Attributes
    ----------
    __connection : Union[psycopg2.extensions.connection, None]
        SQLite connection

    """

    # ============================ MAGIC METHODS =================================

    def __init__(self,
                 dbname="postgres",
                 user="postgres",
                 password=None,
                 host="127.0.0.1",
                 port="5432",
                 template: DBTemplateType = None):
        """
        Initialization

        Parameters
        ----------

        template : DBTemplateType
            template of database structure (DBTemplateType)

        """

        #        __slots__ = ('__path', '__connection') # Memory optimisation !!!

        super(PostgreSQLx, self).__init__(placeholder='%s')

        self.__dbname = dbname
        self.__user = user
        self.__host = host
        self.__port = port

        self.__connection = None       # init connection
        self.connect(password=password)# creating connection with db

        if template:
            self.markup(template=template)

    def __str__(self):
        return f"<PostgreSQLx: {{dbname: {self.dbname}, user: {self.user}, {self.host}:{self.port}}}>"

    def __bool__(self):
        try:
            return bool(self.pragma("database_list"))
        except Exception as error:
            logger.error(error)
            return False

    # =============================== PROPERTIES ==================================

    @property
    def connection(self) -> Union[connection, None]:
        return self.__connection

    @property
    def dbname(self) -> AnyStr:
        return self.__dbname

    @property
    def user(self) -> AnyStr:
        return self.__user

    @property
    def host(self) -> AnyStr:
        return self.__host

    @property
    def port(self) -> AnyStr:
        return self.__port

    # ================================== STMT'S ====================================

    def _pragma_stmt(self, *args: str, **kwargs):
        """

        """
        return super(PostgreSQLx, self)._pragma_stmt(
            *args,
            **kwargs
        )

    def _create_stmt(
            self,
            temp: AnyStr,
            name: AnyStr,
            columns: ColumnsType,
            IF_NOT_EXIST: bool = None,
            without_rowid: bool = None,
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._create_stmt(
            temp=temp,
            name=name,
            columns=columns,
            IF_NOT_EXIST=IF_NOT_EXIST,
            without_rowid=without_rowid
        )

    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @parse.args_parser
    def _insert_stmt(
            self, *args: InsertingData, TABLE: AnyStr, script="", values=(), **kwargs: Any,
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._insert_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs
        )

    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @parse.args_parser
    def _fast_insert_stmt(
            self, *args, TABLE: AnyStr, script="", values=(), **kwargs: Any
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._fast_insert_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs
        )

    @parse.or_param_
    @parse.from_as_
    def _insertmany_stmt(
            self,
            *args: InsertingManyData,
            TABLE: AnyStr,
            script="",
            values=(),
            **kwargs: Any,
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._insertmany_stmt(
            *args,
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs
        )


    @parse.offset_
    @parse.limit_
    @parse.order_by_
    @parse.where_(placeholder='%s')
    @parse.join_
    @parse.with_
    @parse.from_as_
    def _select_stmt(
            self,
            TABLE: Union[str, AbstractTable],
            script="",
            values=(),
            method: AnyStr = "SELECT ",
            SELECT: Union[
                str, AbstractColumn, List[Union[str, AbstractColumn]], Tuple[Union[str, AbstractColumn]]] = None,
            **kwargs,
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._select_stmt(
            TABLE=TABLE,
            script=script,
            values=values,
            method=method,
            SELECT=SELECT,
            **kwargs
        )


    @parse.where_(placeholder='%s')
    @parse.with_
    def _delete_stmt(self, TABLE: str, script="", values=(), **kwargs) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._delete_stmt(
            TABLE=TABLE,
            script=script,
            values=values,
            **kwargs
        )

    @parse.where_(placeholder='%s')
    @parse.or_param_
    @parse.with_
    def _update_stmt(
            self,
            TABLE: AnyStr,
            SET: Union[List, Tuple, Mapping] = None,
            script="",
            values=(),
            **kwargs,
    ) -> ScriptAndValues:
        """

        """
        return super(PostgreSQLx, self)._update_stmt(
            TABLE=TABLE,
            SET=SET,
            script=script,
            values=values,
            **kwargs
        )

    # ============================= ABC PRIVATE METHODS ============================

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
            return middleware.execute(script=script, values=values, connection=self.connection)
        elif spec == 2:
            return middleware.executemany(script=script, values=values, connection=self.connection)
        elif spec == 3:
            return middleware.executescript(script=script, connection=self.connection)

    def _get_table(self, name) -> PostgreSQLxTable:
        super(PostgreSQLx, self)._get_table(name=name)
        return PostgreSQLxTable(db=self, name=name)

    def _get_tables(self) -> Generator[PostgreSQLxTable, None, None]:
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

    # ============================== ABC PUBLIC METHODS ============================

    def connect(self, password: AnyStr):
        """
        Create connection to database

        Creating sqlite3.connect(__str__) connection to interact with database

        """

        if not self.connection:
            self.__connection = psycopg2.connect(
                dbname=self.__dbname,
                user=self.__user,
                password=password,
                host=self.__host,
                port=self.__port
            )

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

    # ========================== ADDITIONAL PUBLIC METHODS =========================

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
            columns_: Tuple[Tuple[str]] = self.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
            columns: Tuple = tuple(map(lambda item: item[0], columns_))

        # except ___.OperationalError:
        #     # Fix for compatibility issues #19, by some reason it can't find PRAGMA_TABLE_INFO table
        #     columns_: Tuple[Tuple[str]] = self.pragma(f"table_info('{table}')")
        #     columns: Tuple = tuple(map(lambda item: item[1], columns_))
        except:
            raise SyntaxError("<<< PRAGMA_TABLE_INFO exception >>>")

        if not columns:
            raise TableInfoError

        return columns


__all__ = [
    "PostgreSQLx",  # lgtm [py/undefined-export]
    "PostgreSQLxTable",  # lgtm [py/undefined-export]
]
