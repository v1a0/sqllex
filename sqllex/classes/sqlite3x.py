from sqllex.exceptions import TableInfoError, ArgumentError
from loguru import logger
from sqllex.constants import *
from sqllex.types_ import *
import sqlite3


def __with__(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        with_dict: dict = kwargs.pop('WITH')

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
    def wrapper(*args, **kwargs):
        if 'where' in kwargs.keys():
            where_dict: dict = kwargs.pop('where')
        else:
            where_dict = {}

        stmt: SQLStatement = func(*args, **kwargs)

        if where_dict:
            stmt.request.script += f"WHERE ({'=?, '.join(wh for wh in where_dict.keys())}=?) "
            stmt.request.values = tuple(list(stmt.request.values) + list(where_dict.values()))

        return stmt

    return wrapper


def __or_param__(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        if 'OR' in kwargs.keys():
            _or = kwargs.pop('OR')

            if _or:
                kwargs.update(
                    {
                        'script': kwargs.get('script') + f"OR {_or}"
                    })

        return func(*args, **kwargs)

    return wrapper


def args_parser(func: callable):
    def wrapper(*args: tuple, **kwargs: dict):
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

        # print('args:', args)
        # print('kwargs: ', kwargs)
        return func(*args, **kwargs)

    return wrapper


def table(col: AnyStr, params: Any):
    if isinstance(params, (str, int, float)):
        params = [f"{params}"]

    if isinstance(params, list):
        return f"{col} {' '.join(param for param in params)},\n"

    if isinstance(params, dict) and col == FOREIGN_KEY:
        res = ''
        for (key, refs) in params.items():
            res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
        return res[:-1]

    else:
        raise TypeError


def crop(columns: Union[tuple, list], values: Union[tuple, list]) -> tuple:
    """
    Converts input lists (columns and values) to the same length for safe insert
    :param columns: List of columns in some FROM
    :param values: Values for insert to some FROM
    :return:Equalized by length lists
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


def __execute__(func: callable):
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


class SQLite3x:
    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        SQLite3x
        :param path: Location of database
        :param template: template of DB structure
        """
        self.path = path
        self.journal_mode(mode="WAL")  # make db little bit faster
        self.foreign_keys(mode="ON")
        if template:
            self.markup(template=template)

    def __str__(self):
        return f"{{SQLite3x: path='{self.path}'}}"

    # def __bool__(self):
    #    try:
    #        return bool(self.execute(script="PRAGMA database_list"))
    #    except ExecuteError:
    #        return False

    @logger.catch
    @__execute__
    def _execute_(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    def execute(self, script: AnyStr, values: tuple = None, request: SQLRequest = None) -> Union[List, None]:
        """
        Child method of _execute_ method
        :param script: single SQLite script, might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full statement
        :return: Database answer if it has
        """
        return self._execute_(script=script, values=values, request=request)

    @logger.catch
    @__executemany__
    def _executemany_(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):

        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    def executemany(self, script: AnyStr, values: tuple = None, request: SQLRequest = None) -> Union[List, None]:
        """
        Child method of __executemany__ method
        :param script: single or multiple SQLite script(s), might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full request
        :return: Database answer if it has
        """
        return self._executemany_(script=script, values=values, request=request)

    @logger.catch
    @__execute__
    def _pragma_(self, *args: str, **kwargs):
        if args:
            script = f"PRAGMA {args[0]}"
        elif kwargs:
            script = f"PRAGMA {list(kwargs.keys())[0]}={list(kwargs.values())[0]}"
        else:
            raise ArgumentError(args_kwargs="Unset", error="No data to execute")

        return SQLStatement(SQLRequest(script), self.path)

    def pragma(self, *args: str, **kwargs) -> Union[List, None]:
        return self._pragma_(*args, **kwargs)

    def foreign_keys(self, mode: Literal["ON", "OFF"]):
        return self.pragma(foreign_keys=mode)

    def journal_mode(self, mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]):
        return self.pragma(journal_mode=mode)

    def table_info(self, table_name: str):
        return self.pragma(f"table_info({table_name})")

    @logger.catch
    @__execute__
    def __create__(self, temp: AnyStr, name: AnyStr, columns: TableType,
                   if_not_exist: bool = None, AS: SQLRequest = None, without_rowid: bool = None):
        """
        Parent method for all CREATE-methods
        """
        content: str = ''
        values = ()

        # AS fork
        if AS:
            # AS fork
            content = AS.script
            values = AS.values
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

    def create_table(self, name: AnyStr, columns: TableType,
                     if_not_exist: bool = None, AS: SQLRequest = None, without_rowid: bool = None):
        """
        CREATE TABLE (IF NOT EXISTS) schema-name.table-name ...
            ... (AS select-stmt)/(column-def table-constraint) (WITHOUT ROWID)
        :param name:
        :param columns:
        :param if_not_exist:
        :param AS:
        :param without_rowid:
        :return:
        """
        self.__create__(temp='', name=name, columns=columns,
                        if_not_exist=if_not_exist, AS=AS, without_rowid=without_rowid)

    def create_temp_table(self, name: AnyStr, columns: TableType, **kwargs):
        """
        CREATE TEMP TABLE (IF NOT EXISTS) schema-name.table-name ...
            ... (AS select-stmt)/(column-def table-constraint) (WITHOUT ROWID)
        :param name:
        :param columns:
        :param if_not_exist:
        :param AS:
        :param without_rowid:
        :return:
        """
        self.__create__(temp='TEMP', name=name, columns=columns, **kwargs)

    def create_temporary_table(self, name: AnyStr, columns: TableType, **kwargs):
        """
        CREATE TEMPORARY TABLE (IF NOT EXISTS) schema-name.table-name ...
            ... (AS select-stmt)/(column-def table-constraint) (WITHOUT ROWID)
        :param name:
        :param columns:
        :param if_not_exist:
        :param AS:
        :param without_rowid:
        :return:
        """
        self.__create__(temp='TEMPORARY', name=name, columns=columns, **kwargs)

    def markup(self, template: DBTemplateType):
        """
        Mark up table by template
        """
        for (table_name, columns) in template.items():
            self.create_table(name=table_name, columns=columns, if_not_exist=True)

    def get_columns(self, table: AnyStr) -> Union[tuple, list]:
        """
        Get list of FROM columns
        :param table: schema-name.table-name or just table-name
        """
        columns = self.table_info(table_name=table)
        if columns:
            return tuple(map(lambda item: item[1], columns))
        else:
            raise TableInfoError

    @__execute__
    @__or_param__
    @__with__
    def __insert_stmt__(self, *args: Any, table: AnyStr, script='', values=(), **kwargs: Any):
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

    @args_parser
    def insert(self, table: AnyStr, *args: InsertData, OR: OrOptionsType = None, WITH: WithType = None,
               **kwargs: Any) -> Union[None, SQLStatement]:
        """
        INSERT data into db's FROM
        :param table: Table name for inserting
        :param OR: Optional parameter. If INSERT failed, type OrOptionsType
        :param WITH: Optional parameter.
        """
        return self.__insert_stmt__(script="INSERT ", OR=OR, table=table, *args, **kwargs, WITH=WITH)

    @args_parser
    def replace(self, table: AnyStr, *args: Any, WITH: WithType = None, **kwargs: Any) -> Union[None, SQLStatement]:
        """
        REPLACE data into db's FROM
        :param table: Table name for inserting
        :param WITH: Optional parameter.
        """
        return self.__insert_stmt__(script="REPLACE ", table=table, *args, **kwargs, WITH=WITH)

    @__executemany__
    def _insertmany_(self, table: AnyStr, *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
                     **kwargs: Any):

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

    def insertmany(self, table: AnyStr, *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
                   **kwargs: Any):
        """
        INSERT many data into db's FROM
        The same as regular insert but for lists of inserts
        :param table: FROM name for inserting
        :param args: 1'st way set values for insert
        :param kwargs: 2'st way set values for insert
        """
        return self._insertmany_(table, *args, **kwargs)

    @__execute__
    @__where__
    @__with__
    def _select_stmt_(self, script='', values=(), method: AnyStr='SELECT', select: Union[List[str], str] = None,
                      table: str = None, **kwargs):
        """
        SELECT data from FROM
        :param select: columns to select, have shadow name in kwargs 'columns'. Value '*' by default
        :param table: FROM for selection, have shadow name in kwargs 'from_table'
        :param where: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        :param kwargs: shadow names holder (columns, from_table)
        :param execute: execute script and return db's answer (True) or return script (False)
        :return: DB answer to or script
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
                  f"{', '.join(sel for sel in select)}" \
                  f" FROM {table} "

        return SQLStatement(SQLRequest(script, values), self.path)

    def select(self, select: Union[List[str], str] = None, FROM: str = None, where: dict = None,
               execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self._select_stmt_(select=select, table=FROM, method='SELECT', where=where, execute=execute,
                                  WITH=WITH, **kwargs)

    def select_distinct(self, select: Union[List[str], str] = None, FROM: str = None, where: dict = None,
                        execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self._select_stmt_(select=select, table=FROM, method='SELECT DISTINCT', where=where, execute=execute,
                                  WITH=WITH, **kwargs)

    def select_all(self, select: Union[List[str], str] = None, FROM: str = None, where: dict = None,
                   execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self._select_stmt_(select=select, table=FROM, method='SELECT ALL ', where=where, execute=execute,
                                  WITH=WITH, **kwargs)

    @__execute__
    @__where__
    @__with__
    def _delete_(self, script='', values=(), table: str = None):
        script += f"DELETE FROM {table} "
        return SQLStatement(SQLRequest(script, values), self.path)

    def delete(self, FROM: str, where: dict = None, WITH: WithType = None, **kwargs):
        return self._delete_(table=FROM, where=where, WITH=WITH, **kwargs)

    # @__execute__
    # @__where__
    # @__or_param__
    # @__with__
    # def _update_(self):
    #
    # def update(self):
    #     pass

# ================================================== #
# ---------------------------------------------------------------------------
# https://www.sitepoint.com/getting-started-sqlite3-basic-commands/
#
#     def update(self):
#         pass
#
#     def drop(self):
#         pass
#
#     def alter(self):
#         # RENAME TO
#         # RENAME COLUMN
#         # ADD COLUMN
#         # https://www.sqlitetutorial.net/sqlite-alter-table/
#         pass
#
#     def commit(self):
#         # ?
#         pass
#
#     def vaccom(self):
#         # https://www.sqlitetutorial.net/sqlite-vacuum/
#         pass


if __name__ == "__main__":
    __all__ = [SQLite3x]
