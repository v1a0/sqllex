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
import sqllex.core.entities.postgresqlx.middleware as middleware
from sqllex.core.tools.docs_helpers import copy_docs

import psycopg2
from psycopg2.extensions import connection


class PostgreSQLxTransaction(AbstractTransaction):
    @property
    def __name__(self):
        return "PostgreSQLxTransaction"


class PostgreSQLxTable(ABTable):
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

        super(PostgreSQLxTable, self).__init__(db=db, name=name)

        if not isinstance(db, PostgreSQLx):
            raise TypeError(f"Argument db have oto be SQLite3x not {type(db)}")
        self.db: PostgreSQLx = db
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


class PostgreSQLx(ABDatabase):
    """
    Main class to interact with PostgreSQL databases.
    It's parent class for PostgreSQLxTable.
    
    (based on AbstractDatabase)
    """

    # ============================ MAGIC METHODS =================================

    def __init__(
            self,
            dbname: AnyStr = "postgres",
            user: AnyStr = "postgres",
            password: AnyStr = None,
            host: AnyStr = "127.0.0.1",
            port: AnyStr = "5432",
            template: DBTemplateType = None,
            init_connection=True,
            connection=None,
            **connection_kwargs
    ):
        """
        Initialization

        Parameters
        ----------
        dbname : AnyStr
            Name of database to connect, "postgres" by default
        user: AnyStr
            Username to login, "postgres" by default
        password: AnyStr
            Password, None by default
        host: AnyStr
            Host address of postgres server, localhost by default
        port: AnyStr
            Port of postgres server, 5432 by default
        template : DBTemplateType
            template of database structure (DBTemplateType)
        init_connection : bool
            Create connection to database with database class object initialisation

        """

        #        __slots__ = ('__path', '__connection') # Memory optimisation !!!

        super(PostgreSQLx, self).__init__(placeholder='%s')

        self.__dbname = dbname
        self.__user = user
        self.__host = host
        self.__port = port

        # connection
        self.__connection = connection  # init connection

        if init_connection and connection_kwargs and self.connection:
            # if connection already exist but func also got an connection_kwargs
            logger.warning(f"Connection already exists, parameters ({connection_kwargs}) have not been set")

        if init_connection:
            try:
                self.connect(password=password, **connection_kwargs)     # creating connection with db
            except TypeError:
                self.connect(**connection_kwargs)

        DEC2FLOAT = psycopg2.extensions.new_type(
            psycopg2.extensions.DECIMAL.values,
            'DEC2FLOAT',
            lambda value, curs: float(value) if value is not None else None
        )

        psycopg2.extensions.register_type(DEC2FLOAT)

        if template:
            self.markup(template=template)

    @copy_docs(ABTable.__str__)
    def __str__(self):
        return f"<PostgreSQLx: {{dbname: {self.dbname}, user: {self.user}, {self.host}:{self.port}}}>"

    @copy_docs(ABTable.__bool__)
    def __bool__(self):
        try:
            return bool(self.connection)
        except Exception as error:
            logger.error(error)
            return False

    # =============================== PROPERTIES ==================================

    @property
    @copy_docs(ABDatabase.connection)
    def connection(self) -> Union[connection, None]:
        return self.__connection

    @property
    def dbname(self) -> AnyStr:
        """
        Name of database to connect, "postgres" by default
        """
        return self.__dbname

    @property
    def host(self) -> AnyStr:
        """
        Host address of postgres server, localhost by default
        """
        return self.__host

    @property
    def port(self) -> AnyStr:
        """
        Port of postgres server, 5432 by default
        """
        return self.__port

    @property
    def user(self) -> AnyStr:
        """
        Username to login, "postgres" by default
        """
        return self.__user

    @property
    def transaction(self) -> PostgreSQLxTransaction:
        return PostgreSQLxTransaction(db=self)

    # ================================== STMT'S ====================================

    @copy_docs(ABDatabase._create_stmt)
    def _create_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._create_stmt(*args, **kwargs)

    @parse.where_(placeholder='%s')
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._insert_stmt)
    def _insert_stmt(self, *args, **kwargs: Any) -> ScriptAndValues:
        return super(PostgreSQLx, self)._insert_stmt(*args, **kwargs)

    @parse.where_(placeholder='%s')
    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._fast_insert_stmt)
    def _fast_insert_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._fast_insert_stmt(*args, **kwargs)

    @parse.where_(placeholder='%s')
    @parse.or_param_
    @parse.from_as_
    @copy_docs(ABDatabase._insertmany_stmt)
    def _insertmany_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._insertmany_stmt(*args, **kwargs)

    @parse.offset_
    @parse.limit_
    @parse.order_by_
    @parse.group_by_
    @parse.where_(placeholder='%s')
    @parse.join_
    @parse.with_
    @parse.from_as_
    @copy_docs(ABDatabase._select_stmt)
    def _select_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._select_stmt(*args, **kwargs)

    @parse.where_(placeholder='%s')
    @parse.with_
    @copy_docs(ABDatabase._delete_stmt)
    def _delete_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._delete_stmt(*args, **kwargs)

    @parse.where_(placeholder='%s')
    @parse.or_param_
    @parse.with_
    @copy_docs(ABDatabase._update_stmt)
    def _update_stmt(self, *args, **kwargs) -> ScriptAndValues:
        return super(PostgreSQLx, self)._update_stmt(*args, **kwargs)

    # ========================= ADDITIONAL STMT'S ====================================
    # None

    # ============================= ABC PRIVATE METHODS ============================

    @copy_docs(ABDatabase._executor)
    def _executor(self, script: AnyStr, values: Tuple = None, spec: Number = 0):
        if spec == 1:
            return middleware.execute(script=script, values=values, connection=self.connection)
        elif spec == 2:
            return middleware.executemany(script=script, values=values, connection=self.connection)
        elif spec == 3:
            return middleware.executescript(script=script, connection=self.connection)

    @copy_docs(ABDatabase._get_table)
    def _get_table(self, name) -> PostgreSQLxTable:
        return PostgreSQLxTable(db=self, name=name)

    @copy_docs(ABDatabase._get_tables)
    def _get_tables(self) -> Generator[PostgreSQLxTable, None, None]:
        for tab_name in self.tables_names:
            yield self._get_table(tab_name)

    @copy_docs(ABDatabase._get_tables_names)
    def _get_tables_names(self) -> Tuple:
        return tuple(map(lambda ret: ret[0], self.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            AND table_type='BASE TABLE'""")))

    # ============================== ABC PUBLIC METHODS ============================

    @copy_docs(ABDatabase.connect)
    def connect(
            self,
            password: AnyStr,
            dbname=None,
            user=None,
            host=None,
            port=None,
            **kwargs
    ):
        """
        Creating psycopg2.extensions.connection to interact with database

        Optional parameters (default):
            dbname=self.dbname,
            user=self.user,
            host=self.host,
            port=self.port,

        Additional kwargs for psycopg2.connect()
            dsn=None,
            connection_factory=None,
            cursor_factory=None,

        """
        if dbname is None:
            dbname = self.dbname
        if user is None:
            user = self.user
        if host is None:
            host = self.host
        if port is None:
            port = self.port

        if not self.connection:
            self.__connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                **kwargs
            )
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

    # ========================== ADDITIONAL PUBLIC METHODS =========================

    @copy_docs(ABDatabase.get_columns_names)
    def get_columns_names(
            self,
            table: AnyStr
    ) -> Tuple:

        columns_: Tuple[Tuple] = self.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        columns: Tuple = tuple(map(lambda item: item[0], columns_))

        if not columns:
            raise TableNotExist(f"No columns or table {table}")

        return columns


__all__ = [
    "PostgreSQLx",  # lgtm [py/undefined-export]
    "PostgreSQLxTable",  # lgtm [py/undefined-export]
    "PostgreSQLxTransaction",  # lgtm [py/undefined-export]
]
