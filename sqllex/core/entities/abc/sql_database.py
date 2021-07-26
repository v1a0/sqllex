# Here is contains Abstract Base Classes for Parent Database Classes
#
# - AbstractDatabase
# + - AbstractTable
#   + - AbstractColumn
#     + - SearchCondition
#

from abc import ABC, abstractmethod
from sqllex.debug import logger
from sqllex.types.types import *
from sqllex.constants.sql import *
import sqllex.core.entities.abc.script_gens as script_gen
from sqllex.core.tools.convertors import crop
import sqllex.core.tools.sorters as sort
import sqllex.core.tools.parsers.parsers as parse
import sqlite3
from sqllex.core.entities.abc.sql_column import SearchCondition
from sqllex.exceptions import TableInfoError
from sqllex.core.entities.abc.sql_column import AbstractColumn





class AbstractTable(ABC):
    """
    Sub-class of AbstractDatabase, itself one table of Database
    Have same methods but without table name argument

    Attributes
    ----------
    db : AbstractDatabase
        AbstractDatabase database object
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
        return self.name

    def __bool__(self):
        return bool(self.get_columns_names())

    def __getitem__(self, key) -> AbstractColumn:
        if key not in self.columns_names:
            raise KeyError(key, "No such column in table")

        return AbstractColumn(table=self.name, name=key)

    @property
    def columns(self) -> Generator[AbstractColumn, None, None]:
        for column in self.columns_names:
            yield AbstractColumn(table=self.name, name=column)

    @property
    def columns_names(self) -> List:
        return self.get_columns_names()

    @abstractmethod
    def info(self):
        """
        Send PRAGMA request table_info(table_name)

        Returns
        ----------
        list
            All information about table

        """

        # return self.db.pragma(f"table_info({self.name})")
        pass

    def add_column(self, column: ColumnsType) -> None:
        """
        Adds column to the table

        Parameters
        ----------
        column : Dict
            Column name and SQL type e.g. {'value': TEXT}

        Returns
        ----------
        None

        """

        self.db.add_column(table=self.name, column=column)

    def remove_column(self, column: Union[AnyStr, AbstractColumn]) -> None:
        """
        Removes column from the table

        Parameters
        ----------
        column : Union[AnyStr, AbstractColumn]
            Name of column or AbstractColumn object.

        Returns
        ----------
        None

        """

        self.db.remove_column(self.name, column)

    def has_column(self, column: Union[AnyStr, AbstractColumn]) -> bool:
        """
        Checks if column exists in the table

        Parameters
        ----------
        column : Union[AnyStr, AbstractColumn]
            Name of column or AbstractColumn object.

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
            SELECT: Union[str, AbstractColumn, List[Union[str, AbstractColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[Tuple, List[List[Any]]]:
        """
        SELECT data from table

        Parameters
        ----------
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
            SELECT: Union[str, AbstractColumn, List[Union[str, AbstractColumn]]] = None,
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


class AbstractDatabase(ABC):

    @abstractmethod
    def __init__(self):
        self.__connection = None

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __bool__(self):
        pass

    @property
    def connection(self):
        return self.__connection

    @property
    def tables(self) -> Generator[AbstractTable, None, None]:
        return self._get_tables()

    @property
    def tables_names(self) -> Tuple[str]:
        return self._get_tables_names()

    def __getitem__(self, key) -> AbstractTable:
        return self._get_table(key)

    def __del__(self):
        if self.connection:
            self.disconnect()

        del self  # ?

    # ============================== PRIVATE METHODS ==============================

    @abstractmethod
    def _executor(self, script: AnyStr, values: Tuple = None, spec: Number = 0):
        """
        Execute scripts with values

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
        pass

    @abstractmethod
    def _get_tables(self) -> Generator[AbstractTable, None, None]:
        pass

    @abstractmethod
    def _get_tables_names(self) -> Tuple[str]:
        pass

    @staticmethod
    def _pragma_stmt(*args: str, **kwargs):
        """
        Parent method for all pragma-like methods
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

    @staticmethod
    def _create_stmt(
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

            if isinstance(params, tuple):
                params = list(params)

            # For {'col': [param2, param1]} -> {'col': [param1, param2]}
            if isinstance(params, list):
                params = sorted(params, key=lambda par: sort.column_types(par))
                content += script_gen.column(name=col, params=tuple(params))

            # For {'col': {FK: {a: b}}}
            elif isinstance(params, dict) and col == FOREIGN_KEY:
                res = ""
                for (key, refs) in params.items():
                    res += script_gen.column_with_foreign_key(key=key, table=refs[0], column=refs[1])
                content += res[:-1]

            else:
                raise TypeError(f'Incorrect column "{col}" initialisation')

        script = script_gen.create(
            temp=temp,
            if_not_exist=IF_NOT_EXIST,
            name=name,
            content=content[:-2],
            without_rowid=without_rowid
        )

        return script, values

    @parse.or_param_
    @parse.with_
    @parse.from_as_
    @parse.args_parser
    def _insert_stmt(
            self, *args: Any, TABLE: AnyStr, script="", values=(), **kwargs: Any,
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
            insert_values = tuple(kwargs.values())

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        script = f"{script}{script_gen.insert(columns=_columns, table=TABLE, need_space=bool(script))}"
        values += insert_values

        return script, values

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

        script = script_gen.insert_fast_with_prefix(
            script=script,
            table=TABLE, placeholders=len(args), need_space=bool(script)
        )
        values += args

        return script, values

    @parse.or_param_
    @parse.from_as_
    @parse.args_parser
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



        if args:
            args = tuple(filter(lambda ar: len(ar) > 0, args[0]))  # removing [] (empty lists from inserting values)

            if len(args) == 0:  # if args empty after filtering, break the function, yes it'll break
                logger.warning("insertmany/updatemany failed, due to no values to insert/update")
                return None, None


            if isinstance(args[0], list):
                args = tuple(
                    map(lambda arg: tuple(arg), args)
                )   # converting lists in args to tuples ([1,2],) -> ((1,2),)

            max_arg_len = max(map(lambda arg: len(arg), args))  # max len of arg in values
            min_arg_len = min(map(lambda arg: len(arg), args))  # min len of arg in values

            temp_ = tuple(0 for _ in range(max_arg_len))   # (1, 'Alex', 'Django')


        elif kwargs:
            for _, arg in kwargs.items():
                args += (tuple(arg),)

            args = tuple(zip(*args))

            columns = tuple(kwargs.keys())

            max_arg_len = max(map(lambda arg: len(arg), args))     # max len of arg in values
            min_arg_len = min(map(lambda arg: len(arg), args))     # min len of arg in values\\

            temp_ = dict(zip(columns, (None,)*len(columns)))  # {'column_1': None, 'column_2': None, 'column_3': None}

        else:
            raise ValueError(f"No data to insert, args: {args}, kwargs: {kwargs}")

        script, expected_values = self._insert_stmt(temp_, script=script, TABLE=TABLE)  # getting stmt for maxsize value

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

    @parse.offset_
    @parse.limit_
    @parse.order_by_
    @parse.where_
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
    ):
        """
        Parent method for all SELECT-like methods

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

        script += script_gen.select(method=method, columns=SELECT, table=TABLE)

        return script, values

    @parse.where_
    @parse.with_
    def _delete_stmt(self, TABLE: str, script="", values=(), **kwargs):
        """
        Parent method for delete method

        """

        script = f"{script}{script_gen.delete(table=TABLE)}"
        return script, values

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
                script += f"'{key.name}'="
            else:
                script += f"'{key}'="

            if isinstance(val, SearchCondition):
                script += f"{val}, "
                values = values + val.values
            else:
                script += "?, "
                values = values + (val,)

        script = script[:-2]

        return script, values

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

        script += script_gen.drop(table=TABLE, if_exist=IF_EXIST)

        return self.execute(script=script)

    # ============================== PUBLIC METHODS ==============================

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def execute(
            self,
            script: AnyStr = None,
            values: Tuple = None,
    ) -> Union[Tuple, None]:
        """
        Execute any SQL-script whit (or without) values, or execute SQLRequest

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains placeholders
        values : Tuple
            Values for placeholders if script contains it

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._executor(script=script, values=values, spec=1)

    def executemany(
            self,
            script: AnyStr = None,
            values: Tuple[Tuple] = None,
    ) -> Union[Tuple, None]:
        """
        Execute any SQL-script for many values sets, or execute SQLRequest

        Parameters
        ----------
        script : AnyStr
            single or multiple SQLite script(s), might contains placeholders
        values : Tuple[Tuple]
            Values for placeholders if script contains it

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._executor(script=script, values=values, spec=2)

    def executescript(
            self,
            script: AnyStr = None,
    ) -> Union[Tuple, None]:
        """
        Execute many SQL-scripts whit (or without) values

        Parameters
        ----------
        script : AnyStr
            single SQLite script, might contains placeholders

        Returns
        ----------
        Union[List, None]
            Database answer if it has

        """

        return self._executor(script=script, spec=3)

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
        Union[List, None]
            Database answer if it has

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

        return self.execute(script=script, values=values)

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
        column : ColumnDataType
            Columns of table (ColumnsType-like)
            Column name and SQL type e.g. {'value': INTEGER}

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

        Returns
        ----------
        None
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

        return self._get_table(name=name)

    def get_columns(
            self,
            table: AnyStr
    ) -> Generator[AbstractColumn, None, None]:
        """
        Get list of table columns like an SQLite3xColumn objects

        Parameters
        ----------
        table : AnyStr
            Name of table

        Returns
        ----------
        Generator[AbstractColumn]
            Columns of table

        """

        try:
            columns_: Tuple[Tuple] = self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")
            columns: Tuple = tuple(map(lambda item: item[0], columns_))

        except sqlite3.OperationalError:
            # Fix for compatibility issues #19, by some reason it can't find PRAGMA_TABLE_INFO table
            columns_: Tuple[Tuple] = self.pragma(f"table_info('{table}')")
            columns: Tuple = tuple(map(lambda item: item[1], columns_))

        if not columns:
            raise TableInfoError(f"No columns or table {table}")

        for column in columns:
            yield AbstractColumn(table=table, name=column)

    @abstractmethod
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
        pass

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
                script, values = self._fast_insert_stmt(
                    *args,
                    script="INSERT",
                    OR=OR,
                    TABLE=TABLE,
                    **kwargs,
                    WITH=WITH,
                )

                self.execute(script=script, values=values)

            else:
                raise ValueError

        except (sqlite3.OperationalError, ValueError):
            script, values = self._insert_stmt(
                *args,
                script="INSERT",
                OR=OR,
                TABLE=TABLE,
                **kwargs,
                WITH=WITH,
            )

            self.execute(script=script, values=values)

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
                script, values = self._fast_insert_stmt(
                    *args,
                    script="REPLACE",
                    TABLE=TABLE,
                    **kwargs,
                    WITH=WITH,
                )

                self.execute(script=script, values=values)

            else:
                raise ValueError

        except (sqlite3.OperationalError, ValueError):
            script, values = self._insert_stmt(
                *args,
                script="REPLACE",
                TABLE=TABLE,
                **kwargs,
                WITH=WITH
            )

            self.execute(script=script, values=values)

    def insertmany(
            self,
            TABLE: AnyStr,
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
            Optional parameter. If INSERT failed, type OrOptionsType
        kwargs : Any
            An 2'st way set values for insert

        Returns
        ----------
            None or SQL-script in SQLStatement

        """

        if len(args) > 1:
            args = [args]

        script, values = self._insertmany_stmt(
            args,
            TABLE=TABLE,
            OR=OR,
            script="INSERT",
            values=(),
            **kwargs
        )

        self.executemany(script=script, values=values)

    def select(
            self,
            TABLE: Union[str, List[str], AbstractTable] = None,
            SELECT: Union[str, AbstractColumn, List[Union[str, AbstractColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], AbstractTable] = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            _method="SELECT",
            **kwargs,
    ) -> Union[Tuple, List[Any]]:
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
            **kwargs,
        )

        return self.execute(script=script, values=values)

    def select_distinct(
            self,
            TABLE: Union[str, List[str], AbstractTable] = None,
            SELECT: Union[str, AbstractColumn, List[Union[str, AbstractColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], AbstractTable] = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[Tuple, List[Any]]:
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
            TABLE: Union[str, List[str], AbstractTable] = None,
            SELECT: Union[str, AbstractColumn, List[Union[str, AbstractColumn]]] = None,
            WHERE: WhereType = None,
            WITH: WithType = None,
            ORDER_BY: OrderByType = None,
            LIMIT: LimitOffsetType = None,
            OFFSET: LimitOffsetType = None,
            FROM: Union[str, List[str], AbstractTable] = None,
            JOIN: Union[str, List[str], List[List[str]]] = None,
            **kwargs,
    ) -> Union[Tuple, List[Any]]:
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

        script, values = self._delete_stmt(
            TABLE=TABLE,
            WHERE=WHERE,
            WITH=WITH,
        )

        self.execute(script, values)

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
