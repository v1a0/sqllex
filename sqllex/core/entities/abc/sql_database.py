"""
AbstractTable and AbstractDatabase
"""
from abc import ABC, abstractmethod
from sqllex.debug import logger
from sqllex.types.types import *
from sqllex.constants import FOREIGN_KEY, ALL, REPLACE
import sqllex.core.entities.abc.script_gens as script_gen
from sqllex.core.tools.convertors import crop
import sqllex.core.tools.sorters as sort
from sqllex.core.entities.abc.sql_column import SearchCondition
from sqllex.core.entities.abc.sql_column import AbstractColumn
from sqlite3 import OperationalError


class AbstractTable(ABC):
    """
    Sub-class of AbstractDatabase, itself one table inside ABDatabase
    Have same methods but without table name argument

    """

    def __init__(self, db, name: AnyStr):
        """
        Parameters
        ----------
        db : AbstractDatabase
            AbstractDatabase database object
        name : str
            Name of table
        """
        
        if not isinstance(db, AbstractDatabase):
            raise TypeError(f"Argument db have oto be AbstractDatabase not {type(db)}")
        self.db: AbstractDatabase = db
        self.name: AnyStr = name

    def __str__(self):
        """
        Convert database object to string
        """
        return self.name

    def __bool__(self):
        """
         Convert database object to boolean
        """
        return bool(self.get_columns_names())

    def __getitem__(self, key) -> AbstractColumn:
        """
        Get column from table
            table['column_name']
            db['table_name']['column_name']
        """
        if key not in self.columns_names:
            raise KeyError(key, f"No such column '{key}' in table '{self.name}'")

        return AbstractColumn(table=self.name, name=key)

    @property
    def columns(self) -> Generator[AbstractColumn, None, None]:
        """
        Get all columns of table
        """
        for column in self.columns_names:
            yield AbstractColumn(table=self.name, name=column)

    @property
    def columns_names(self) -> Tuple:
        """
        Get names of table columns
        """
        return self.get_columns_names()

    def add_column(self, column: ColumnsType) -> None:
        """
        Adds column to the table

        Parameters
        ----------
        column : ColumnsType
            ColumnType tuple like {'second_name': [TEXT, UNIQUE]}
        """
        self.db.add_column(table=self.name, column=column)

    def remove_column(self, column: Union[AnyStr, AbstractColumn]) -> None:
        """
        Removes column from the table

        Parameters
        ----------
        column : Union[AnyStr, AbstractColumn]
            Name of column or column-object to remove
        """
        
        self.db.remove_column(self.name, column)

    def has_column(self, column: Union[AnyStr, AbstractColumn]) -> bool:
        """
        Checks if column exists in the table

        Parameters
        ----------
        column : Union[AnyStr, AbstractColumn]
            Name of column or column-object.

        Returns
        ----------
        bool
            logical value of column's existence.

        """

        if isinstance(column, AbstractColumn):
            column = column.name

        if column in self.columns_names:
            return True

        return False

    def get_columns_names(self) -> Tuple[str]:
        """
        Get list of table columns

        Returns
        ----------
        Tuple[str]
            All table's columns

        """
        return self.db.get_columns_names(table=self.name)

    # ======================== MAIN COMMON METHODS ========================

    def insert(
            self,
            *args: InsertingData,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            **kwargs: Any,
    ) -> None:
        """
        INSERT data into table

        Parameters
        ----------
        args : InsertingData
            Inserting data-set
        OR : OrOptionsType
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        WITH : WithType
            Disabled!
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
        """

        self.db.replace(self.name, *args, **kwargs)

    def insertmany(
            self,
            *args: InsertingManyData,
            OR: OrOptionsType = None,
            **kwargs: Any,
    ) -> None:
        """
        INSERT many data into table.
        The same as regular insert but for lists of inserting values

        Parameters
        ----------
        args : Union[List, Tuple]
            1'st way set values for insertion
            > ((1, 'Alex'), (2, 'Bob'))
        OR : OrOptionsType
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        kwargs : Any
            2'nd way set values for insertion
            id=(1, 2), name=('ALex', 'Bob')

        """

        self.db.insertmany(self.name, *args, OR=OR, **kwargs)

    def select(
            self,
            SELECT: Union[
                AnyStr, AbstractColumn, ConstantType,
                List[Union[AbstractColumn, AnyStr]], Tuple[Union[AbstractColumn, AnyStr]]
            ] = None,
            WHERE: Union[WhereType, SearchCondition] = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: JoinArgType = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        SELECT data from table

        Parameters
        ----------
        SELECT : Union[str, List[str]]
            columns to select. Value '*' by default
            > SELECT=['id', 'name']
        WHERE : WhereType
            optional parameter for conditions
            > db: AbstractDatabase
            > ...
            > WHERE=(db['table_name']['column_name'] == 'some_value')
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10
        OFFSET : LimitOffsetType
            Set offset for selecting records
            > OFFSET=5
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],
        GROUP_BY: Union[GroupByType, AbstractColumn]
            optional parameter for group data in database response

        Returns
        ----------
        Tuple[Tuple]
            Selected records

        """

        return self.db.select(
            self.name,
            SELECT=SELECT,
            WHERE=WHERE,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            GROUP_BY=GROUP_BY,
            **kwargs,
        )

    def select_distinct(
            self,
            SELECT: Union[
                AnyStr, AbstractColumn, ConstantType,
                List[Union[AbstractColumn, AnyStr]], Tuple[Union[AbstractColumn, AnyStr]]
            ] = None,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        return self.db.select_distinct(
            self.name,
            SELECT=SELECT,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            GROUP_BY=GROUP_BY,
            **kwargs,
        )

    def select_all(
            self,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        SELECT ALL data from table

        Parameters
        ----------
        WHERE : WhereType
            optional parameter for conditions
            > db: AbstractDatabase
            > ...
            > WHERE=(db['table_name']['column_name'] == 'some_value')
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10
        OFFSET : LimitOffsetType
            Set offset for selecting records
            > OFFSET=5
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],
        GROUP_BY: Union[GroupByType, AbstractColumn]
            optional parameter for group data in database response

        Returns
        ----------
        Tuple[Tuple]
            Selected records

        """

        return self.db.select_all(
            self.name,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            GROUP_BY=GROUP_BY,
            **kwargs,
        )

    def delete(
            self,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
        """
        DELETE FROM table

        Parameters
        ----------
        WHERE : WhereType
           optional parameter for conditions
           > WHERE=(db['table_name']['column_name'] == 'some_value')

        """

        self.db.delete(
            self.name, WHERE=WHERE, WITH=WITH, **kwargs
        )

    def update(
            self,
            SET: Union[List, Tuple, Mapping],
            WHERE: Union[WhereType, SearchCondition] = None,
            OR: OrOptionsType = None,
            WITH: WithType = None,
            **kwargs,
    ) -> None:
        """
        UPDATE, SET column_name=something WHERE x=y and more complex requests

        Parameters
        ----------
        SET : Union[List, Tuple, Mapping]
            ColumnType and value to set
        WHERE : WhereType
            optional parameter for conditions
            > WHERE=(db['table_name']['column_name'] == 'some_value')
        OR : OrOptionsType
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        WITH : WithType
            Disabled!
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
            WHERE: Union[WhereType, SearchCondition] = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        Find all records in table where_

        Parameters
        ----------
        WHERE : WhereType
           optional parameter for conditions
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10

        **kwargs : Any
            You can also set where condition by kwargs
            > name="MyName", age=42 

        Returns
        ----------
        List[List]
            Selected data
        """
        if not WHERE:
            WHERE = kwargs

        return self.select_all(WHERE=WHERE, ORDER_BY=ORDER_BY, LIMIT=LIMIT)


class AbstractDatabase(ABC):
    """
    Main Abstract Parent class for any database.
    Contains basic common databases properties and methods
    used as base for all sqllex database classes

    Abstract/Regular Magic Methods (amm/_mm)
        amm/ __init__
        amm/ __str__
        amm/ __bool__
        _mm/ __getitem__
        _mm/ __del__

    Properties (__p)
        __p/ connection
        __p/ tables
        __p/ tables_names

    Abstract/Regular Private Methods (axm/_xm)
        axm/ _executor
        axm/ _get_table
        axm/ _get_tables
        axm/ _get_tables_names

    Statements Constructor (__s)
        __s/ _create_stmt
        __s/ _insert_stmt
        __s/ _fast_insert_stmt
        __s/ _insertmany_stmt
        __s/ _select_stmt
        __s/ _delete_stmt
        __s/ _update_stmt
        __s/ _drop_stmt

    Abstract/Regular Public Methods (apm/_pm)
        apm/ connect
        apm/ disconnect
        apm/ get_columns_names
        _pm/ execute > _executor
        _pm/ executemany > _executor
        _pm/ executescript > _executor
        _pm/ create_table > _create_stmt > execute
        _pm/ create_temp_table > _create_stmt > execute
        _pm/ create_temporary_table > _create_stmt > execute
        _pm/ markup > create_table
        _pm/ add_column > execute
        _pm/ remove_column > execute
        _pm/ get_table > _get_table > execute
        _pm/ get_columns > execute
        _pm/ insert > _fast_insert_stmt / _insert_stmt > execute
        _pm/ replace > _fast_insert_stmt / _insert_stmt > execute
        _pm/ insertmany > _insertmany_stmt > execute
        _pm/ select > _select_stmt > execute
        _pm/ select_distinct > select
        _pm/ select_all > select
        _pm/ delete > _delete_stmt > execute
        _pm/ update > _update_stmt > execute
        _pm/ updatemany > _insertmany_stmt > execute
        _pm/ drop > _drop_stmt > execute

    """

    @abstractmethod
    def __init__(self, placeholder):
        """
        Init-ing database, connection, creating connection, setting parameters
        """

        self.__connection = None
        self.__placeholder = placeholder

    @abstractmethod
    def __str__(self):
        """
        ABDatabase as string
        """
        pass

    @abstractmethod
    def __bool__(self):
        """
        Is connection or database exist
        """
        pass

    def __getitem__(self, key) -> AbstractTable:
        """
        Get table from database
            db['table_name']
        """
        if key not in self.tables_names:
            raise KeyError(key, f"No such table '{key}' in database")

        return self._get_table(key)

    def __del__(self):
        """
        Death of database object
        """
        if self.connection:
            self.disconnect()




    @property
    @abstractmethod
    def connection(self):
        """
        Get connection as object
        """
        return self.__connection

    @property
    def tables(self) -> Generator[AbstractTable, None, None]:
        """
        Get generator of all tables as objects
        """
        return self._get_tables()

    @property
    def tables_names(self) -> Tuple[str]:
        """
        Get names of all tables
        """
        return self._get_tables_names()

    @property
    def placeholder(self) -> str:
        """
        Placeholder symbol
        """
        return self.__placeholder

    @property
    @abstractmethod
    def transaction(self):
        """
        Property to create transaction statement. Have to be used inside 'with' statement.

            >>> import sqllex as sx
            >>>
            >>> db = sx.SQLite3x('some.db')
            >>>
            >>> with db.transaction as tran:
            >>>    try:
            >>>        # Transaction body
            >>>        # db.execute(...)
            >>>        ...
            >>>        tran.commit() # optional
            >>>
            >>>    except Exception:
            >>>        tran.rollback()  # rollback transaction is something goes wrong
        """

        return

    # ============================== PRIVATE METHODS ==============================

    @abstractmethod
    def _executor(self, script: AnyStr, values: Tuple = None, spec: Number = 0):
        """
        Execute scripts with (or without) values

        Parameters
        ----------
        spec : Number
            Id of execution case:
                1. Regular execute
                2. Executemany
                3. Executescript
        """
        pass

    @abstractmethod
    def _get_table(self, name):
        """
        Get specific table as SQLite3xTable objects
        """
        pass

    @abstractmethod
    def _get_tables(self) -> Generator[AbstractTable, None, None]:
        # for tab_name in self.tables_names:
        #     yield self._get_table(tab_name)
        pass

    @abstractmethod
    def _get_tables_names(self) -> Tuple[str]:
        """
        Generator of tables as SQLite3xTable objects

        Returns
        ----------
        Tuple[str]
            list of tables names
        """
        pass

    # ================================ STMT'S =========================================

    @staticmethod
    def _create_stmt(
            temp: AnyStr,
            name: AnyStr,
            columns: ColumnsType,
            IF_NOT_EXIST: bool = None,
            without_rowid: bool = None,
    ) -> ScriptAndValues:
        """
        Constructor of create-like statements
        """

        def content_gen(parameters, column=None) -> str:

            if isinstance(parameters, str):
                """
                {
                    'col': "INTEGER",
                }
                """
                return script_gen.column(name=column, params=(parameters,))

            elif isinstance(parameters, list):
                """
                {
                    'col': ["INTEGER", "NOT NULL"],
                }
                """
                parameters = sorted(parameters, key=lambda par: sort.column_types(par))
                return script_gen.column(name=column, params=tuple(parameters))

            elif isinstance(parameters, tuple):
                """
                {
                    'col': ("INTEGER", "NOT NULL"),
                }
                """
                parameters = sorted(list(parameters), key=lambda par: sort.column_types(par))
                return script_gen.column(name=column, params=tuple(parameters))

            elif isinstance(parameters, dict):
                """
                {
                    FOREIGN_KEY: {
                        "group_id": ["groups", "group_id"]
                    }
                }
                """
                if column != FOREIGN_KEY:
                    raise TypeError(f'Incorrect column "{column}" initialisation: {parameters}')

                res = ""
                for (key, refs) in parameters.items():
                    if isinstance(refs, (list, tuple)):
                        res += script_gen.column_with_foreign_key(key=key, table=refs[0], column=refs[1])
                    if isinstance(refs, AbstractColumn):
                        res += script_gen.column_with_foreign_key(key=key, table=refs.table, column=refs.name)

                return res[:-1]

            else:
                raise TypeError(f'Incorrect column "{column}" initialisation, parameters type {type(parameters)}, '
                                f'expected tuple, list or str')

        if not columns:
            raise ValueError("Zero-column tables aren't supported in SQLite")

        content = ""
        values = ()

        for (col, params) in columns.items():
            content += content_gen(params, column=col)

        script = script_gen.create(
            temp=temp,
            if_not_exist=IF_NOT_EXIST,
            name=name,
            content=content[:-2],
            without_rowid=without_rowid
        )

        return script, values

    def _insert_stmt(
            self, data: Union[Tuple, List, Mapping], TABLE: Union[AnyStr, AbstractTable], script="", values=(),
            OR: OrOptionsType = None, WITH: WithType = None, WHERE: Union[WhereType, SearchCondition] = None
    ) -> ScriptAndValues:
        """
        Constructor of insert/replace statements

        Creating insert/replace stmt with specified columns names
        """

        if isinstance(data, (tuple, list)):
            _columns = self.get_columns_names(table=TABLE)
            _columns, insert_values = crop(_columns, tuple(data))

        elif isinstance(data, dict):
            _columns = tuple(data.keys())
            insert_values = tuple(data.values())

        else:
            raise ValueError(f"No data to insert, data: {data}")

        script = script_gen.insert(script=script, columns=_columns, table=TABLE, placeholder=self.placeholder)
        values += insert_values

        return script, values


    def _fast_insert_stmt(
            self, data: Union[Tuple, List], TABLE: Union[AnyStr, AbstractTable], script="", values=(),
            OR: OrOptionsType = None, WITH: WithType = None, WHERE: Union[WhereType, SearchCondition] = None
    ) -> ScriptAndValues:
        """
        Constructor of fast insert/replace statements

        Creating insert/replace stmt without columns names
        (without get_columns_names request, because it's slow)
        """

        script = script_gen.insert_fast_with_prefix(
            script=script,
            table=TABLE, ph_amount=len(data), need_space=bool(script), placeholder=self.placeholder
        )
        values += tuple(data)

        return script, values

    def _insertmany_stmt(
            self,
            *args: InsertingManyData,
            TABLE: Union[AnyStr, AbstractTable],
            script="",
            values=(),
            OR=None,
            **kwargs: Any,
    ) -> ScriptAndValues:
        """
        Constructor of insertmany statements

        Comment:
            args also support numpy.array value

        """

        if args:
            args = tuple(filter(lambda ar: len(ar) > 0, args[0]))  # removing [] (empty lists from inserting values)

            if len(args) == 0:  # if args empty after filtering, break the function, yes it'll break
                logger.warning("insertmany/updatemany failed, due to no values to insert/update")
                return '', tuple()

            if isinstance(args[0], list):
                args = tuple(
                    map(lambda arg: tuple(arg), args)
                )  # converting lists in args to tuples ([1,2],) -> ((1,2),)

            max_arg_len = max(map(lambda arg: len(arg), args))  # max len of arg in values
            min_arg_len = min(map(lambda arg: len(arg), args))  # min len of arg in values

            temp_ = tuple(0 for _ in range(max_arg_len))


        elif kwargs:
            for _, arg in kwargs.items():
                args += (tuple(arg),)

            args = tuple(zip(*args))

            columns = tuple(kwargs.keys())

            max_arg_len = max(map(lambda arg: len(arg), args))  # max len of arg in values
            min_arg_len = min(map(lambda arg: len(arg), args))  # min len of arg in values\\

            temp_ = dict(zip(columns, (None,) * len(columns)))  # {'column_1': None, 'column_2': None, 'column_3': None}

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        script, expected_values = self._insert_stmt(data=temp_, script=script, TABLE=TABLE)  # getting stmt for maxsize value

        possible_len = len(expected_values)  # len of max supported val list

        if min_arg_len != possible_len or max_arg_len != possible_len:
            # if some inserting datasets have different length
            # crop or append these sets

            cropped_values = tuple()

            for arg in args:  # cropping or appending args, making it's same size
                # arg: tuple
                if len(arg) == possible_len:
                    cropped_values += (arg,)
                if len(arg) < possible_len:
                    cropped_values += (arg + ((None,) * (possible_len - len(arg))),)
                elif len(arg) > possible_len:
                    cropped_values += (arg[:possible_len],)

            values += cropped_values

        else:
            values += args

        return script, values

    def _select_stmt(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            script="",
            values=(),
            method: AnyStr = "SELECT ",
            SELECT: Union[
                AnyStr,
                AbstractColumn, ConstantType,
                List[Union[AnyStr, AbstractColumn]],
                Tuple[Union[AnyStr, AbstractColumn]]
            ] = None,
            **kwargs,
    ) -> ScriptAndValues:
        """
        Constructor of select(-like) statements
        """
        
        if not TABLE:
            raise ValueError("Argument TABLE unset and have not default value")

        if SELECT is None:
            if method != "SELECT ALL ":
                logger.warning("Argument SELECT not specified, default value is '*'")
            SELECT = ("*",)

        elif isinstance(SELECT, (str, AbstractColumn)):
            SELECT = (SELECT,)

        elif isinstance(SELECT, list):
            SELECT = (*SELECT,)

        script += script_gen.select(method=method, columns=SELECT, table=str(TABLE))

        return script, values

    def _delete_stmt(self, TABLE: str, script="", values=(), **kwargs) -> ScriptAndValues:
        """
        Constructor of delete statements
        """

        script = script_gen.delete(script=script, table=TABLE)
        return script, values

    def _update_stmt(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            SET: Union[List, Tuple, Mapping] = None,
            script="",
            values=(),
            **kwargs,
    ) -> ScriptAndValues:
        """
        Constructor of update statements
        """

        script = script_gen.update_script(table=TABLE, script=script)

        if not SET and kwargs:
            SET = kwargs

        # if set is not {'column': (val1, val2)}
        # [column1, val1, column2, val2]
        if isinstance(SET, list):
            SET = tuple(SET)

        # (column1, val1, column2, val2)
        if isinstance(SET, tuple):
            new_set = {}

            if len(SET) % 2 == 0:  # for ['name', 'Alex', 'age', 2]
                for i in range(len(SET) // 2):
                    new_set.update({SET[2 * i]: SET[2 * i + 1]})

            else:
                raise TypeError

            SET: dict = new_set

        for (key, val) in SET.items():
            if issubclass(type(key), AbstractColumn):
                script += f'"{key.name}"='
            else:
                script += f'"{key}"='

            if isinstance(val, SearchCondition):
                script += f"{val}, "
                values = values + val.values
            else:
                script += f"{self.placeholder}, "
                values = values + (val,)

        script = script[:-2]

        return script, values

    @staticmethod
    def _drop_stmt(
            TABLE: Union[AnyStr, AbstractTable],
            IF_EXIST: bool = True,
            script="",
            **kwargs
    ) -> AnyStr:
        """
        Constructor of drop statements
        """

        script += script_gen.drop(table=TABLE, if_exist=IF_EXIST)

        return script

    # ============================== PUBLIC METHODS ==============================

    @abstractmethod
    def connect(self, *args, **kwargs):
        """
        Create connection if it does not exist
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Discard connection if it is exist
        """
        pass

    def execute(
            self,
            script: AnyStr = None,
            values: Tuple = None,
    ) -> Union[Tuple, List, None]:
        """
        Execute any SQL-script whit (or without) values

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains ph_amount
        values : Tuple
            Values for ph_amount if script contains it

        Returns
        ----------
        Union[Tuple, None]
            ABDatabase answer if it has

        """

        return self._executor(script=script, values=values, spec=1)

    def executemany(
            self,
            script: AnyStr = None,
            values: Tuple = None,
    ) -> Union[Tuple, List, None]:
        """
        Execute any SQL-script for many values sets

        Parameters
        ----------
        script : AnyStr
            single or multiple SQLite script(s), might contains ph_amount
        values : Tuple[Tuple]
            Values for ph_amount if script contains it

        Returns
        ----------
        Union[Tuple, None]
            ABDatabase answer if it has

        """

        return self._executor(script=script, values=values, spec=2)

    def executescript(
            self,
            script: AnyStr = None,
    ) -> Union[Tuple, List, None]:
        """
        Execute many SQL-scripts whit (or without) values

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains ph_amount

        Returns
        ----------
        Union[Tuple, None]
            ABDatabase answer if it has

        """

        return self._executor(script=script, spec=3)

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

        script, values = self._create_stmt(
            temp="",
            name=name,
            columns=columns,
            IF_NOT_EXIST=IF_NOT_EXIST,
            without_rowid=without_rowid,
        )

        self.execute(script=script, values=values)

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

        script, values = self._create_stmt(
            temp="TEMP",
            name=name,
            columns=columns,
            **kwargs
        )

        return self.execute(script=script, values=values)

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

        script, values = self._create_stmt(
            temp="TEMPORARY",
            name=name,
            columns=columns,
            **kwargs
        )

        return self.execute(script=script, values=values)

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

    def add_column(  # !!!
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
        column : ColumnType
            Columns of table (ColumnsType-like)
            ColumnType name and SQL type e.g. {'value': INTEGER}

        Returns
        ----------
        None
        """

        for (column_name, column_type) in column.items():
            if not isinstance(column_type, (list, tuple)):
                column_type = (column_type,)

            self.execute(
                f"ALTER TABLE "
                f"'{table}' "
                f"ADD "
                f"'{column_name}' "
                f"{' '.join(ct for ct in column_type)}")

    def remove_column(  # !!!
            self,
            table: AnyStr,
            column: Union[AnyStr, AbstractColumn]
    ):
        """
        Removes column from the table

        Parameters
        ----------
        table : AnyStr
            Name of table
        column : Union[AnyStr, AbstractColumn]
            Name of column or AbstractColumn object.

        """

        column_name = column

        if isinstance(column, AbstractColumn):
            column_name = column.name

        self.execute(
            f"ALTER TABLE '{table}' "
            f"DROP COLUMN '{column_name}'"
        )

    def get_table(
            self,
            name: AnyStr
    ) -> AbstractTable:
        """
        Shadow method for __getitem__, that used as like: database['table_name']

        Get table object (AbstractTable instance)

        Parameters
        ----------
        name : AnyStr
            Name of table

        Returns
        ----------
        AbstractTable
            Instance of AbstractTable, table of database

        """

        return self.__getitem__(key=name)

    def get_columns(
            self,
            table: AnyStr
    ) -> Generator[AbstractColumn, None, None]:
        """
        Get columns of table as AbstractColumns objects

        Parameters
        ----------
        table : AnyStr
            Name of table

        Returns
        ----------
        Tuple
            Columns of table as AbstractColumns objects

        """
        columns = self.get_columns_names(table=table)

        for column in columns:
            yield AbstractColumn(table=table, name=column)

    @abstractmethod
    def get_columns_names(
            self,
            table: AnyStr
    ) -> Tuple:
        """
        Get list of names of table columns as strings

        Parameters
        ----------
        table : AnyStr
            Name of table

        Returns
        ----------
        Tuple[str]
            Columns of table

        """
        pass

    def insert(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            *args: InsertingData,
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
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        WITH : WithType
            Disabled!

        """

        if args:
            if isinstance(args[0], (tuple, list, dict)):
                data = args[0]
            else:
                data = args
        elif kwargs:
            data = kwargs
        else:
            raise ValueError("No data to insert")

        try:
            if isinstance(data, (tuple, list)):
                script, values = self._fast_insert_stmt(
                    data=data,
                    TABLE=TABLE,
                    script="INSERT",
                    OR=OR,
                    WITH=WITH,
                )

                self.execute(script=script, values=values)

            else:
                raise ValueError("No arguments for fast insertion")

        except (OperationalError, ValueError):
            script, values = self._insert_stmt(
                data=data,
                TABLE=TABLE,
                script="INSERT",
                OR=OR,
                WITH=WITH,
            )

            self.execute(script=script, values=values)

    def replace(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            *args: Any,
            WHERE: Union[WhereType, SearchCondition] = None,
            **kwargs: Any,
    ) -> None:
        """
        REPLACE data into table

        Parameters
        ----------
        TABLE : AnyStr
            Name of table
        WHERE : WhereType
            Optional parameter for conditions
            > WHERE=(db['table_name']['column_name'] == 'some_value')

        """

        if args:
            if isinstance(args[0], (tuple, list, dict)):
                data = args[0]
            else:
                data = args
        elif kwargs:
            data = kwargs
        else:
            raise ValueError("No data to insert")

        try:
            if args:
                script, values = self._fast_insert_stmt(
                    data=data,
                    script="REPLACE",
                    TABLE=TABLE,
                    WHERE=WHERE,
                )

                self.execute(script=script, values=values)

            else:
                raise ValueError("No arguments for fast insertion")

        except (OperationalError, ValueError):
            script, values = self._insert_stmt(
                data=data,
                script="REPLACE",
                TABLE=TABLE,
                WHERE=WHERE,
            )

            self.execute(script=script, values=values)

    def insertmany(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            *args: Union[List[List], List[Tuple], Tuple[List], Tuple[Tuple], List, Tuple, Iterable],
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
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        if len(args) > 1:
            script, values = self._insertmany_stmt(
                args,
                TABLE=TABLE,
                OR=OR,
                script="INSERT",
                values=(),
                **kwargs
            )

        else:
            script, values = self._insertmany_stmt(
                *args,
                TABLE=TABLE,
                OR=OR,
                script="INSERT",
                values=(),
                **kwargs
            )

        self.executemany(script=script, values=values)

    def select(
            self,
            TABLE: Union[AnyStr, AbstractTable] = None,
            SELECT: Union[AnyStr, AbstractColumn, ConstantType, List, Tuple] = None,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], Tuple[str], AbstractTable] = None,
            JOIN: JoinArgType = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            _method="SELECT",
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        SELECT data from table

        Parameters
        ----------
        TABLE: Union[AnyStr, AbstractTable]
            Name of table
        SELECT : Union[str, List[str]]
            columns to select. Value '*' by default
            > SELECT=['id', 'name']
        WHERE : WhereType
           optional parameter for conditions
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        WITH : WithType
            Disabled!
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10
        OFFSET : LimitOffsetType
            Set offset for selecting records
            > OFFSET=5
        FROM : str
            Name of table, same at TABLE
        JOIN: JoinArgType
            optional parameter for joining data from other tables ['groups'],
        GROUP_BY: Union[GroupByType, AbstractColumn]
            optional parameter for group data in database response
        _method: str
            DON'T CHANGE IT! special argument for unite select_all, select_distinct into select()

        Returns
        ----------
        Tuple[Tuple]
            Tuple of Selected data

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

        script, values = self._select_stmt(
            SELECT=SELECT,
            TABLE=TABLE,
            method=_method,
            WHERE=WHERE,
            WITH=WITH,
            ORDER_BY=ORDER_BY,
            LIMIT=LIMIT,
            OFFSET=OFFSET,
            JOIN=JOIN,
            GROUP_BY=GROUP_BY,
            **kwargs,
        )

        return self.execute(script=script, values=values)

    def select_distinct(
            self,
            TABLE: Union[AnyStr, AbstractTable] = None,
            SELECT: Union[str, AbstractColumn, ConstantType, Tuple, List] = None,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], Tuple[str], AbstractTable] = None,
            JOIN: JoinArgType = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        SELECT distinct from table

        Parameters
        ----------
        TABLE : Union[str, List[str], AbstractTable]
            Name of table
        SELECT : Union[str, AbstractColumn, Tuple, List]
            columns to select. Value '*' by default
        WHERE : WhereType
           optional parameter for conditions
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        WITH : WithType
            Disabled!
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10
        OFFSET : LimitOffsetType
            Set offset for selecting records
            > OFFSET=5
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],
        GROUP_BY: Union[GroupByType, AbstractColumn]
            optional parameter for group data in database response
        FROM : str
            Name of table, same at TABLE

        Returns
        ----------
        Tuple[Tuple]
            Selected data

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
            GROUP_BY=GROUP_BY,
            **kwargs
        )

    def select_all(
            self,
            TABLE: Union[AnyStr, AbstractTable] = None,
            SELECT: Union[str, AbstractColumn, ConstantType, List, Tuple] = None,
            WHERE: Union[WhereType, SearchCondition] = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], Tuple[str], AbstractTable] = None,
            JOIN: JoinArgType = None,
            GROUP_BY: Union[GroupByType, AbstractColumn] = None,
            **kwargs,
    ) -> Tuple[Tuple]:
        """
        SELECT all data from table

        Parameters
        ----------
        TABLE : Union[str, AbstractTable]
            Name of table
        SELECT : Union[str, AbstractColumn, List, Tuple]
            columns to select. Value '*' by default
        WHERE : WhereType
           optional parameter for conditions
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        WITH : WithType
            Disabled!
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        ORDER_BY : OrderByType
            optional parameter for conditions
            > ORDER_BY=['age', 'DESC']
            > ORDER_BY='age DESC'
        LIMIT: LimitOffsetType
            Set limit or selecting records
            > LIMIT=10
        OFFSET : LimitOffsetType
            Set offset for selecting records
            > OFFSET=5
        JOIN: Union[str, List[str], List[List[str]]]
            optional parameter for joining data from other tables ['groups'],
        GROUP_BY: Union[GroupByType, AbstractColumn]
            optional parameter for group data in database response
        FROM : Union[str, List[str], AbstractTable]
            Name of table, same at TABLE

        Returns
        ----------
        Tuple[Tuple]
            Selected data

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
            GROUP_BY=GROUP_BY,
            **kwargs
        )

    def delete(
            self,
            TABLE: str,
            WHERE: Union[WhereType, SearchCondition] = None,
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
           optional parameter for conditions
           > db: AbstractDatabase
           > ...
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        WITH : WithType
            Disabled!

        """

        if not WHERE:
            WHERE = kwargs

        script, values = self._delete_stmt(
            TABLE=TABLE,
            WHERE=WHERE,
            WITH=WITH,
        )

        self.execute(script, values)

    def update(
            self,
            TABLE: Union[AnyStr, AbstractTable],
            SET: Union[List, Tuple, Mapping],
            WHERE: Union[WhereType, SearchCondition] = None,
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
            ColumnType and value to set
        WHERE : WhereType
           optional parameter for conditions
           > db: AbstractDatabase
           > ...
           > WHERE=(db['table_name']['column_name'] == 'some_value')
        OR : OrOptionsType
            Action in case if inserting has failed. Optional parameter.
            > OR='IGNORE'
        WITH : WithType
            Disabled!
        """

        if not WHERE:
            WHERE = kwargs

        script, values = self._update_stmt(
            TABLE=TABLE,
            SET=SET,
            OR=OR,
            WHERE=WHERE,
            WITH=WITH,
            **kwargs,
        )

        self.execute(script=script, values=values)

    def updatemany(
            self,
            TABLE: Union[AnyStr, AbstractTable],
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

        if SET is None:
            # In case if SET == []
            logger.warning(
                f"AbstractDatabase.updatemany "
                f"got empty list of data to update or got nothing at all, "
                f"{SET=}"
            )

        else:
            script, values = self._insertmany_stmt(
                SET,
                TABLE=TABLE,
                script="INSERT",
                OR=REPLACE,
                **kwargs,
            )

            self.executemany(script=script, values=values)

    def drop(
            self,
            TABLE: Union[AnyStr, AbstractTable],
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

        script = self._drop_stmt(
            TABLE=TABLE,
            IF_EXIST=IF_EXIST,
            **kwargs
        )

        self.execute(script=script)
