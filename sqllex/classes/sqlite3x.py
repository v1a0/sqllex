from sqllex.exceptions import TableInfoError, ArgumentError, ExecuteError
from loguru import logger
from sqllex.constants.sql import *
from sqllex.types_.types import *
import sqlite3


def __with__(func: callable) -> callable:
    """
    Decorator for catching WITH argument

    If it has, adding into beginning of :script: with_statement.

    And adding values into :values: if it has

    :kwarg with_: Mapping[str, SQLRequest]

    """

    def wrapper(*args, **kwargs):
        with_dict: Mapping[str, SQLRequest] = kwargs.pop('with_')

        if with_dict:
            script = f"WITH "
            values = []

            for (var, statement) in with_dict.items():

                # Checking is value of dict SQLStatement or str
                if issubclass(type(statement), SQLStatement):
                    condition = statement.request
                elif isinstance(statement, str):
                    condition = statement
                else:
                    raise TypeError

                if issubclass(type(condition), SQLRequest):
                    script += f"{var} AS ({condition.script}), "
                    values += list(condition.values)
                else:
                    script += f"{var} AS ({condition}), "

            kwargs.update(
                {
                    'values': tuple(values) if not kwargs.get('values') else
                    tuple(list(kwargs.get('values')) + list(values)),

                    'script': f"{script[:-2]} " if not kwargs.get('script') else
                    f"{script[:-2]} " + kwargs.get('script')
                })

            return func(*args, **kwargs)

        return func(*args, **kwargs)

    return wrapper


def __where__(func: callable) -> callable:
    """
        Decorator for catching WHERE argument

        If it has, adding into end of :script: where_statement

        And adding values into :values: if it has

        where : Mapping[str, SQLRequest]

    """
    def wrapper(*args, **kwargs):
        if 'where' in kwargs.keys():
            where_dict: Mapping[str, SQLRequest] = kwargs.pop('where')
        else:
            where_dict = {}

        stmt: SQLStatement = func(*args, **kwargs)

        if where_dict:
            stmt.request.script += f"WHERE ({'=? AND '.join(wh for wh in where_dict.keys())}=?) "
            stmt.request.values = tuple(list(stmt.request.values) + list(where_dict.values()))

        return stmt

    return wrapper


def __or_param__(func: callable) -> callable:
    """
        Decorator for catching OR argument

        If it has, adding into beginning of :param script: or_statement

        or_ : OrOptionsType

    """

    def wrapper(*args, **kwargs):
        if 'or_' in kwargs.keys():
            _or: OrOptionsType = kwargs.pop('or_')

            if _or:
                kwargs.update(
                    {
                        'script': kwargs.get('script') + f"OR {_or}"
                    })

        return func(*args, **kwargs)

    return wrapper


def __order_by__(func: callable) -> callable:
    """
        Decorator for catching order_by argument

        If it has, adding into beginning of :param script: order_by_statement

        order_by : OrderByType

    """

    def wrapper(*args, **kwargs):
        if 'order_by' in kwargs.keys():
            order_by: OrderByType = kwargs.pop('order_by')
        else:
            order_by = False

        stmt: SQLStatement = func(*args, **kwargs)

        if order_by:
            if isinstance(order_by, (str, int)):
                stmt.request.script += f"ORDER BY {order_by} "
            elif isinstance(order_by, (list, tuple)):
                stmt.request.script += f"ORDER BY {', '.join(str(item_ob) for item_ob in order_by)} "
            elif isinstance(order_by, dict):
                for (key, val) in order_by.items():
                    if isinstance(val, (str, int)):
                        uni_val = f"{val} "
                    elif isinstance(val, (list, tuple)):
                        uni_val = ' '.join(sub_val for sub_val in val)
                    else:
                        raise TypeError

                    stmt.request.script += f"ORDER BY {key} {uni_val} "

        return stmt

    return wrapper


def __limit__(func: callable) -> callable:
    """
        Decorator for catching limit argument

        If it has, adding into beginning of :param limit: order_by_statement

        limit : OrderByType

    """

    def wrapper(*args, **kwargs):
        if 'limit' in kwargs.keys():
            limit: LimitOffsetType = kwargs.pop('limit')
        else:
            limit: bool = False

        stmt: SQLStatement = func(*args, **kwargs)

        if limit:
            if isinstance(limit, (float, str)):
                limit = int(limit)
            stmt.request.script += f"LIMIT {limit} "

        return stmt

    return wrapper


def __offset__(func: callable) -> callable:
    """
        Decorator for catching limit argument

        If it has, adding into beginning of :param limit: order_by_statement

        limit : OrderByType

    """

    def wrapper(*args, **kwargs):
        if 'offset' in kwargs.keys():
            offset: LimitOffsetType = kwargs.pop('offset')
        else:
            offset: bool = False

        stmt: SQLStatement = func(*args, **kwargs)

        if offset:
            if isinstance(offset, (float, str)):
                offset = int(offset)
            stmt.request.script += f"OFFSET {offset} "

        return stmt

    return wrapper


def __execute__(func: callable):
    """
        Decorator for execute SQLStatement

        execute : Boolean parameter setting execute script or not, if True - executing script with values
        elif False - return script with values as SQLStatement()

        :return: SQLStatement or None

    """

    def wrapper(*args: tuple, **kwargs: dict):

        if 'execute' in kwargs.keys():
            execute = bool(kwargs.pop('execute'))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)

        if not execute:
            return stmt

        print(stmt.request.script, stmt.request.values if stmt.request.values else '', '\n')
        with sqlite3.connect(stmt.path) as conn:
            cur = conn.cursor()

            try:
                if stmt.request.values:
                    cur.execute(stmt.request.script, stmt.request.values)
                else:
                    cur.execute(stmt.request.script)
                conn.commit()

                return cur.fetchall()

            except Exception as error:
                raise error

    return wrapper


def __executemany__(func: callable):
    """
        Decorator for executemany SQLStatement with multiple of values

        execute : Boolean parameter setting execute script or not, if True - executing script with values
        elif False - return script with values as SQLStatement()

        :return: SQLStatement or None

    """

    def wrapper(*args: tuple, **kwargs: dict):
        if 'execute' in kwargs.keys():
            execute = bool(kwargs.pop('execute'))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)

        if not execute:
            return stmt

        print(stmt.request.script, stmt.request.values if stmt.request.values else '', '\n')
        with sqlite3.connect(stmt.path) as conn:
            cur = conn.cursor()
            cur.executemany(stmt.request.script, stmt.request.values)
            conn.commit()

            return cur.fetchall()

    return wrapper


def tuples_to_lists(func: callable) -> callable:
    """
        Decorator for executes, List(tuples) -> List(list)


        if execute returns values as answer of database, for example select-like methods
        it'll convert List(tuples) to List(list)

        :return: SQLStatement or List[Lists]

    """

    def wrapper(*args, **kwargs):
        ret_ = func(*args, **kwargs)
        if isinstance(ret_, list):
            return list(map(lambda item:
                            list(item) if len(item) > 1 else list(item)[0],
                            func(*args, **kwargs)))
        else:
            return ret_

    return wrapper


def args_parser(func: callable):
    """
        Arguments parser

        If func got only one argument which contains args for function it'll unwrap it

        if args is dict :
            return args = None, kwargs = args[0]

        if args is list :
            return args = args[0], kwargs = kwargs

        if args is tuple :
            return args = list(args[0]), kwargs = kwargs

    """

    def wrapper(*args: Any, **kwargs: Any):
        if args:
            arg0 = list(args)[0]
            args = list(args)[1:]

            if len(args) == 1:
                if isinstance(args[0], dict):
                    args, kwargs = None, args[0]
                elif isinstance(args[0], list):
                    args, kwargs = args[0], kwargs
                elif isinstance(args[0], tuple):
                    args, kwargs = list(args[0]), kwargs

            else:
                for arg in args:
                    if isinstance(arg, dict):
                        kwargs.update(arg)
                        print(arg)
                        args.remove(arg)

            args = (arg0, *args)

        return func(*args, **kwargs)

    return wrapper


def crop(columns: Union[tuple, list], values: Union[tuple, list]) -> tuple:
    """
        Converts input lists (columns and values) to the same length for safe insert

        :param columns: List of columns in some table
        :param values: Values for insert to some table

        :return: Equalized by length lists

    """
    if values and columns:
        if len(values) != len(columns):
            logger.warning(
                f"\n"
                f"SIZE CROP! Expecting {len(columns)} arguments but {len(values)} were given!\n"
                f"Expecting: {columns}\n"
                f"Given: {values}"
            )
            _len_ = min(len(values), len(columns))
            return columns[:_len_], values[:_len_]

    return columns, values



class SQLite3x:
    """
        SQLite3x Excellent Database Class

        :param path: Local path to database (PathType)
        :param template: template of database structure (DBTemplateType)

        https://www.sqlite.org/lang.html

    """

    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
            Initialization
        """
        self.path = path
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

    # ============================== PRIVATE METHODS ==============================

    @logger.catch
    @__execute__
    def _execute_stmt_(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):
        """
            Parent method for execute
        """
        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    @logger.catch
    @__executemany__
    def _executemany_stmt(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):
        """
            Parent method for executemany
        """
        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    @logger.catch
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

        return SQLStatement(SQLRequest(script), self.path)

    @logger.catch
    @__execute__
    def _create_stmt_(self, temp: AnyStr, name: AnyStr, columns: ColumnsType, if_not_exist: bool = None,
                      as_: SQLRequest = None, without_rowid: bool = None):
        """
            Parent method for all CREATE-methods
        """
        content: str = ''
        values = ()

        # AS fork
        if as_:
            # AS fork
            content = as_.script
            values = as_.values
        else:
            # column-def
            for (col, params) in columns.items():
                if isinstance(params, (str, int, float)):
                    params = [f"{params}"]

                if isinstance(params, list):
                    # column-def, table-constraint
                    content += f"{col} {' '.join(param for param in params)},\n"

                elif isinstance(params, dict) and col == FOREIGN_KEY:
                    res = ''
                    for (key, refs) in params.items():
                        res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
                    content += res[:-1]

                else:
                    raise TypeError

            content = f"{content[:-2]}"

        script = f"CREATE " \
                 f"{temp} " \
                 f" TABLE " \
                 f"{'IF NOT EXISTS' if if_not_exist else ''} " \
                 f"'{name}' " \
                 f" (\n{content}\n) " \
                 f"{'WITHOUT ROWID' if without_rowid else ''};"

        return SQLStatement(SQLRequest(script=script, values=values), self.path)

    @__execute__
    @__or_param__
    @__with__
    def _insert_stmt_(self, *args: Any, table: AnyStr, script='', values=(), **kwargs: Any):
        """
            INSERT INTO request (aka insert-stmt) and REPLACE INTO request
        """
        values = list(values)

        # parsing args or kwargs for _columns and insert_values
        if args:
            if isinstance(list(args)[0], (list, tuple)):  # if args[0] : list or tuple
                args = list(args)[0]
            if isinstance(args, (str, int)):  # if args contains only one argument
                args = list(args)

            _columns = self.get_columns(table=table)
            _columns, args = crop(_columns, args)
            insert_values = args

        elif kwargs:
            _columns = tuple(kwargs.keys())
            insert_values = list(kwargs.values())

        else:
            raise ArgumentError(args_kwargs="Unset", error="No data to insert")

        script += f"{' ' if script else ''}" \
                  f"INTO {table} (" \
                  f"{', '.join(column for column in _columns)}) " \
                  f"VALUES (" \
                  f"{', '.join('?' * len(insert_values))}) "

        all_values = tuple(values) + tuple(insert_values)

        return SQLStatement(SQLRequest(script, tuple(value for value in all_values)), self.path)

    @__executemany__
    def _insertmany_stmt_(self, table: AnyStr, *args: Union[list[list], list[tuple], tuple[list], tuple[tuple],
                                                            list, tuple], **kwargs: Any):
        """
            Parent method for insertmany
        """
        if args:
            values = list(map(lambda arg: list(arg), args))  # make values list[list] (yes it's necessary)

            if len(values) == 1 and isinstance(values[0], list):
                values = values[0]

            max_l = max(map(lambda arg: len(arg), values))  # max len of arg in values
            temp_ = [0 for _ in range(max_l)]  # example values [] for script
            stmt = self.insert(table, temp_, execute=False)
            _len = len(stmt.request.values)

            for i in range(len(values)):
                while len(values[i]) < _len:
                    values[i] += [None]
                while len(values[i]) > _len:
                    values[i] = values[i][:_len]

        elif kwargs:
            temp_ = {}
            values = []
            columns = list(kwargs.keys())
            args = list(map(lambda vals: list(vals), kwargs.values()))

            for i in range(len(args)):
                temp_[columns[i]] = args[i][0]

            stmt = self.insert(table, temp_, execute=False)
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

        values = tuple(map(lambda arg: tuple(arg), values))  # make values tuple[tuple] (yes it's necessary)

        return SQLStatement(SQLRequest(stmt.request.script, values), self.path)

    @tuples_to_lists
    @__execute__
    @__offset__
    @__limit__
    @__order_by__
    @__where__
    @__with__
    def _select_stmt_(self, script='', values=(), method: AnyStr = 'SELECT ', select: Union[List[str], str] = None,
                      table: str = None, **kwargs):
        """
            Parent method for all SELECT-like methods
        """
        if kwargs:
            if kwargs.get('from_table'):
                table = kwargs.pop('from_table')
            if kwargs.get('columns'):
                select = kwargs.pop('columns')

        if not table:
            raise ArgumentError(from_table="Argument unset and have not default value")

        if select is None:
            logger.warning(ArgumentError(select="Argument not specified, default value is '*'"))
            select = ['*']

        elif isinstance(select, str):
            select = [select]

        script += f"{method} " \
                  f"{', '.join(sel for sel in select)} " \
                  f"FROM {table} "

        return SQLStatement(SQLRequest(script, values), self.path)

    @__execute__
    @__where__
    @__with__
    def _delete_stmt_(self, script='', values=(), table: str = None):
        """
            Parent method for DELETE method
        """
        script += f"DELETE FROM {table} "
        return SQLStatement(SQLRequest(script, values), self.path)

    @__execute__
    @__where__
    @__or_param__
    @__with__
    def _update_stmt_(self, table: AnyStr, set_: Union[list, tuple, dict], script='', values=(), from_as=None,
                      **kwargs):
        """
            Parent method for UPDATE
        """

        if from_as is None:
            from_as = {}
        if not set_ and kwargs:
            set_ = kwargs
        if isinstance(set_, dict):
            set_ = [list(set_.keys())[0], list(set_.values())[0]]
        elif isinstance(set_, tuple):
            set_ = list(set_)

        values += tuple(list(values) + [set_[1]])

        if from_as:
            fa_script = list(from_as.values())[0].script
            fa_var = list(from_as.keys())[0]
            fa_values = list(from_as.values())[0].values
            values += tuple(list(values) + list(fa_values))
        else:
            fa_script = ''
            fa_var = ''

        script += f"UPDATE {table} " \
                  f"SET {set_[0]} = (?) " \
                  f"{f'FROM {fa_script} AS {fa_var} ' if (fa_script and fa_var) else ''}"

        return SQLStatement(SQLRequest(script=script, values=values), self.path)

    @__execute__
    def _drop_stmt_(self, table: AnyStr, if_exist: bool = True, script='', **kwargs):
        """
            Parent method for drop
        """
        script += f"DROP TABLE " \
                  f"{'IF EXISTS' if if_exist else ''} " \
                  f"{table} "
        return SQLStatement(SQLRequest(script=script), self.path)

    # ============================== PUBLIC METHODS ==============================

    def execute(self,
                script: AnyStr,
                values: tuple = None,
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

    def executemany(self,
                    script: AnyStr,
                    values: tuple = None,
                    request: SQLRequest = None
                    ) -> Union[List, None]:
        """
            Child method of __executemany__ method

            :param script: single or multiple SQLite script(s), might contains placeholders
            :param values: Values for placeholders if script contains it
            :param request: Instead of script and values might execute full request

            :return: Database answer if it has

        """
        return self._executemany_stmt(script=script, values=values, request=request)

    def pragma(self,
               *args: str,
               **kwargs
               ) -> Union[List, None]:
        """
            Set PRAGMA params

            :param args: Might be execute like this:
                            > db.pragma("database_list")
            :param kwargs: Might be set like this:
                            > db.pragma(foreign_keys="ON")

        """
        return self._pragma_stmt_(*args, **kwargs)

    def foreign_keys(self,
                     mode: Literal["ON", "OFF"]
                     ):
        """
            Turn on/off PRAGMA param FOREIGN KEYS

            :param mode: "ON" or "OFF"

        """
        return self.pragma(foreign_keys=mode)

    def journal_mode(self,
                     mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
                     ):
        """
            Set PRAGMA param journal_mode

            :param mode: "DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"

        """
        return self.pragma(journal_mode=mode)

    def table_info(self,
                   table_name: str
                   ):
        """
            Send PRAGMA request table_info(table_name)

            :param table_name: Name of table

        """

        return self.pragma(f"table_info({table_name})")

    def create_table(self,
                     name: AnyStr,
                     columns: ColumnsType,
                     if_not_exist: bool = None,
                     as_: SQLRequest = None,
                     without_rowid: bool = None
                     ):
        """
            CREATE TABLE table-name

            Optional:
                CREATE TABLE (IF NOT EXISTS) schema-name.table-name
                (AS select-stmt) / (column-def table-constraint) (WITHOUT ROWID)

            :param name: Table name
            :param columns: Columns of table (ColumnsType)
            :param if_not_exist: Turn on/off "IF NOT EXISTS" prefix
            :param as_:
            :param without_rowid:

        """
        self._create_stmt_(temp='', name=name, columns=columns,
                           if_not_exist=if_not_exist, as_=as_, without_rowid=without_rowid)

    def create_temp_table(self,
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
        self._create_stmt_(temp='TEMP', name=name, columns=columns, **kwargs)

    def create_temporary_table(self,
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
        self._create_stmt_(temp='TEMPORARY', name=name, columns=columns, **kwargs)

    def markup(self,
               template: DBTemplateType
               ):
        """
            Mark up table by template

            :param template: Structure of database (DBTemplateType)

        """
        for (table_name, columns) in template.items():
            self.create_table(name=table_name, columns=columns, if_not_exist=True)

    def get_columns(self,
                    table: AnyStr
                    ) -> Union[tuple, list]:
        """
            Get list of table columns

            :param table: schema-name.table-name or just table-name

            :return: List[List] of columns
        """
        columns = self.table_info(table_name=table)
        if columns:
            return tuple(map(lambda item: item[1], columns))
        else:
            raise TableInfoError

    @args_parser
    def insert(self,
               table: AnyStr,
               *args: InsertData,
               or_: OrOptionsType = None,
               with_: WithType = None,
               **kwargs: Any
               ) -> Union[None, SQLStatement]:
        """
            INSERT data into db's table

            :param table: Table name for inserting
            :param or_: Optional parameter. If INSERT failed, type OrOptionsType
            :param with_: Optional parameter.

        """
        return self._insert_stmt_(script="INSERT ", or_=or_, table=table, *args, **kwargs, with_=with_)

    @args_parser
    def replace(self,
                table: AnyStr,
                *args: Any,
                with_: WithType = None,
                **kwargs: Any
                ) -> Union[None, SQLStatement]:
        """
            REPLACE data into db's table

            :param table: Table name for inserting
            :param with_: Optional parameter.

        """
        return self._insert_stmt_(script="REPLACE ", table=table, *args, **kwargs, with_=with_)

    def insertmany(self,
                   table: AnyStr,
                   *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
                   **kwargs: Any
                   ) -> Union[None, SQLStatement]:
        """
            INSERT many data into db's table.
            The same as regular insert but for lists of inserting values

            :param table: table name for inserting
            :param args: 1'st way set values for insert
            :param kwargs: 2'st way set values for insert

        """
        return self._insertmany_stmt_(table, *args, **kwargs)

    def select(self,
               select: Union[List[str], str] = None,
               table: str = None,
               where: dict = None,
               execute: bool = True,
               with_: WithType = None,
               order_by: OrderByType = None,
               limit: LimitOffsetType = None,
               offset: LimitOffsetType = None,
               **kwargs
               ) -> Union[SQLRequest, List[List]]:
        """
            SELECT data from table

            :param select: columns to select. Value '*' by default
            :param table: table for selection
            :param where: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
            :param kwargs: shadow names holder (columns, from_table)
            :param execute: execute script and return db's answer (True) or return script (False)
            :param with_: with_statement
            :param order_by: optional parameter for conditions, example: {'name': ['NULLS', 'LAST']}
            :param limit: optional parameter for conditions, example: 10
            :param offset: optional parameter for conditions, example: 5

            :return: List[List] of selects

        """
        return self._select_stmt_(select=select, table=table, method='SELECT', where=where, execute=execute,
                                  with_=with_, order_by=order_by, limit=limit, offset=offset, **kwargs)

    def select_distinct(self,
                        select: Union[List[str], str] = None,
                        table: str = None, where: dict = None,
                        execute: bool = True,
                        with_: WithType = None,
                        order_by: OrderByType = None,
                        limit: LimitOffsetType = None,
                        offset: LimitOffsetType = None,
                        **kwargs
                        ) -> Union[SQLRequest, List]:
        return self._select_stmt_(select=select, table=table, method='SELECT DISTINCT', where=where, execute=execute,
                                  with_=with_, order_by=order_by, limit=limit, offset=offset, **kwargs)

    def select_all(self,
                   select: Union[List[str], str] = None,
                   table: str = None, where: dict = None,
                   execute: bool = True,
                   with_: WithType = None,
                   order_by: OrderByType = None,
                   limit: LimitOffsetType = None,
                   offset: LimitOffsetType = None,
                   **kwargs
                   ) -> Union[SQLRequest, List]:

        return self._select_stmt_(select=select, table=table, method='SELECT ALL ', where=where, execute=execute,
                                  with_=with_, order_by=order_by, limit=limit, offset=offset, **kwargs)

    def delete(self,
               table: str,
               where: dict = None,
               with_: WithType = None,
               **kwargs
               ) -> Union[None, SQLStatement]:
        """
            DELETE FROM table WHERE {something}

            :param table: Table name as string
            :param where: where_statement
            :param with_: with_statement

        """

        return self._delete_stmt_(table=table, where=where, with_=with_, **kwargs)

    def update(self,
               table: AnyStr,
               set_: Union[list, tuple, dict],
               where: dict,
               or_: OrOptionsType = None,
               execute: bool = True,
               from_as: Mapping[str, SQLRequest] = None,
               with_: WithType = None, **kwargs):
        """
            UPDATE table_name SET column_name=something WHERE x=y and more complex requests

            :param table: Table name
            :param set_: Column and value to set
            :param where: where_statement
            :param or_: Optional parameter. If INSERT failed, type OrOptionsType
            :param execute: execute script and return db's answer (True) or return script (False)
            :param with_: with_statement

        """
        return self._update_stmt_(table=table, set_=set_, or_=or_, where=where, execute=execute,
                                  with_=with_, from_as=from_as, **kwargs)

    def drop(self,
             table: AnyStr,
             if_exist: bool = True,
             execute: bool = True,
             **kwargs
             ):
        """
            DROP TABLE (IF EXIST) table_name

            :param table: Table name
            :param if_exist: Check is table exist (boolean)
            :param execute: execute script and return db's answer (True) or return script (False)
        """
        return self._drop_stmt_(table=table, if_exist=if_exist, execute=execute, **kwargs)


__all__ = ["SQLite3x"]
