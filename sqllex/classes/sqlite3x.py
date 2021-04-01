from sqllex.exceptions import TableInfoError, ExecuteError, ArgumentError
from loguru import logger
from sqllex.constants import *
from sqllex.types_ import *
import sqlite3


def __with__(func: callable) -> callable:
    def wrapper(*args: tuple, **kwargs: dict):
        with_dict: dict = kwargs.pop('WITH')
        if with_dict:
            script = f"WITH "
            values = []

            for (var, condition) in with_dict.items():
                if issubclass(type(condition), SQLRequest):
                    script += f"{var} AS ({condition.script}), "
                    values += list(condition.values)
                else:
                    script += f"{var} AS ({condition}), "

            return func(script=script[:-2], values=values, *args, **kwargs)

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
                        args.remove(arg)

            args = (arg0, *args)

        # print('args:', args)
        # print('kwargs: ', kwargs)
        return func(*args, **kwargs)


    return wrapper


def table(col: AnyStr, params: Any):
    if isinstance(params, list):
        return f"{col} {' '.join(param for param in params)},\n"

    elif isinstance(params, str):
        return f"{col} {params}" + ',\n'

    elif isinstance(params, (int, float)):
        return f"{col} {params}" + ',\n'

    if isinstance(params, dict) and col == FOREIGN_KEY:
        res = ''
        for (key, refs) in params.items():
            res += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]}), \n"
        return res[:-1]

    else:
        raise TypeError


def quote(val: Union[int, float, str, list, type, list]):
    """
    Quotes control
    :param: Any val
    :return str(val) if value not (int or in CONSTANTS )
    """
    if isinstance(val, (int, float)) or val in CONSTANTS:
        return val

    elif isinstance(val, (list, tuple)) and len(val) == 1:
        return f'{val[0]}'

    else:
        return f'{val}'


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


def __new_execute__(func: callable):
    def wrapper(*args: tuple, **kwargs: dict):

        stmt: SQLStatement = func(*args, **kwargs)

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


def __new_executemany__(func: callable):
    def wrapper(*args: tuple, **kwargs: dict):
        stmt: SQLStatement = func(*args, **kwargs)

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
            self.__markup__(template=template)

    def __str__(self):
        return f"{{SQLite3x: path='{self.path}'}}"

    def __bool__(self):
        try:
            return bool(self.execute(script="PRAGMA database_list"))
        except ExecuteError:
            return False

    @__new_execute__
    def execute(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):
        """
        Child method of __execute__ method
        :param script: single SQLite script, might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full statement
        :return: Database answer if it has
        """
        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    @logger.catch
    @__new_executemany__
    def executemany(self, script: AnyStr, values: tuple = None, request: SQLRequest = None):
        """
        Child method of __executemany__ method
        :param script: single or multiple SQLite script(s), might contains placeholders
        :param values: Values for placeholders if script contains it
        :param request: Instead of script and values might execute full request
        :return: Database answer if it has
        """
        if not request:
            return SQLStatement(SQLRequest(script, values), self.path)
        else:
            return SQLStatement(request, self.path)

    @__new_execute__
    def pragma(self, *args: str, **kwargs):
        if args:
            script = f"PRAGMA {args[0]}"
        elif kwargs:
            script = f"PRAGMA {list(kwargs.keys())[0]}={list(kwargs.values())[0]}"
        else:
            raise ArgumentError(args_kwargs="Unset", error="No data to execute")

        return SQLStatement(SQLRequest(script), self.path)

    def foreign_keys(self, mode: Literal["ON", "OFF"]):
        return self.pragma(foreign_keys=mode)

    def journal_mode(self, mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]):
        return self.pragma(journal_mode=mode)

    def table_info(self, table_name: str):
        return self.pragma(f"table_info({table_name})")

    @__new_execute__
    def __create__(self, create: AnyStr, name: AnyStr, columns: TableType):
        """
        Create FROM in db
        :param name: FROM name
        :param columns: FROM's columns
        :return:
        """
        result: str = ''

        for (col, params) in columns.items():
            result += table(col=col, params=params)

        return SQLStatement(SQLRequest(script=f'{create} TABLE "{name}" (\n{result[:-2]}\n);'), self.path)







    def create_table(self, name: AnyStr, columns: TableType):
        """
        Create FROM in db
        :param name: FROM name
        :param columns: FROM's columns
        :param safe: Convert not supported types in columns.values() to string, like [1, 2, 3] -> "[1, 2, 3]"
        :return:
        """
        create = "CREATE"
        self.__create__(create=create, name=name, columns=columns)

    def __markup__(self, template: DBTemplateType):
        """Need to rename"""
        for (table, columns) in template.items():
            self.create_table(name=table, columns=columns)

    def get_columns(self, table: AnyStr) -> tuple:
        """
        Get list of FROM columns
        :param table: FROM where from you want to get columns
        :return: [ (cid, name, type, notnull, default val, pk), ... ]
        """
        columns = self.table_info(table_name=table)
        if columns:
            return tuple(map(lambda item: item[1], columns))
        else:
            raise TableInfoError

    @__with__
    def __insert_stmt__(self, method: AnyStr, table: AnyStr, *args: Any, **kwargs: Any):
        """
        INSERT INTO request (aka insert-stmt) and REPLACE INTO request
        """
        if kwargs.get('script'):  # if script has set (and have WITH)
            script = kwargs.pop('script')
            values = kwargs.pop('values')
        else:
            script, values = '', []

        if 'execute' in kwargs.keys():
            execute = bool(kwargs.pop('execute'))
        else:
            execute = True

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
                  f"{method} " \
                  f"INTO {table} (" \
                  f"{', '.join(column for column in _columns)}) VALUES (" \
                  f"{', '.join('?' * len(insert_values))})"

        all_values = tuple(values) + tuple(insert_values)

        return SQLStatement(SQLRequest(script, tuple(value for value in all_values)), self.path)

    @args_parser
    @__new_execute__
    def insert(self, table: AnyStr, *args: InsertData, OR: InsertOrOptions = None, WITH: WithType = None,
               **kwargs: Any) -> SQLStatement:
        """
        INSERT data into db's FROM
        :param table: Table name for inserting
        :param OR: Optional parameter. If INSERT failed, type InsertOrOptions
        :param WITH: Optional parameter.
        """
        if OR:
            method = f'INSERT OR {OR}'
        else:
            method = 'INSERT'

        # kwargs.update({'FROM': FROM})
        return self.__insert_stmt__(method, table, *args, **kwargs, WITH=WITH)


    @args_parser
    def replace(self, table: AnyStr, *args: Any, WITH: WithType = None, **kwargs: Any):
        """
        REPLACE data into db's FROM
        :param table: Table name for inserting
        :param WITH: Optional parameter.
        """
        return self.__insert_stmt__('REPLACE', table, *args, **kwargs, WITH=WITH)

    def insertmany(self, table: AnyStr, *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
                   **kwargs: Any):
        """
        INSERT many data into db's FROM
        The same as regular insert but for lists of inserts
        :param table: FROM name for inserting
        :param args: 1'st way set values for insert
        :param kwargs: 2'st way set values for insert
        """

        if args:
            values = list(map(lambda arg: list(arg), args))  # make values list[list] (yes it's necessary)

            if len(values) == 1 and isinstance(values[0], list):
                values = values[0]

            max_l = max(map(lambda arg: len(arg), values))  # max len of arg in values
            temp_ = [0 for _ in range(max_l)]  # example values [] for script
            exe = self.insert(table, temp_, execute=False)
            len = len(exe.values)

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

            exe = self.insert(table, temp_, execute=False)
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

        self.executemany(exe.script, values)

    @__with__
    def __select_stmt__(self, *args, script='', values=(), select: Union[List[str], str] = None, table: str = None,
                        where: dict = None, execute: bool = True, **kwargs) -> Union[SQLRequest, List]:
        """
                SELECT data from FROM
                :param select: columns to select, have shadow name in kwargs 'columns'. Value '*' by default
                :param table: FROM for selection, have shadow name in kwargs 'from_table'
                :param where: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
                :param kwargs: shadow names holder (columns, from_table)
                :param execute: execute script and return db's answer (True) or return script (False)
                :return: DB answer to or script
                """
        if not where:
            where = {}

        if kwargs:
            if kwargs.get('execute'):
                execute: bool = bool(kwargs.pop('execute'))
            if kwargs.get('from_table'):
                table = kwargs.pop('from_table')
            if kwargs.get('columns'):
                select = kwargs.pop('columns')
            where.update()

        if not table:
            raise ArgumentError(from_table="Argument unset and have not default value")

        if select is None:
            logger.warning(ArgumentError(select="Argument not specified, default value is '*'"))
            select = ['*']

        elif isinstance(select, str):
            select = [select]

        script = ''

        script += f"SELECT " \
                  f"{', '.join(sel for sel in select)}" \
                  f" FROM {table} "

        if where:
            script += f"WHERE ({'=?, '.join(wh for wh in where.keys())}=?)"

        # script += ';\n'

        if execute:
            return self.execute(script, tuple(where.values()))
        else:
            return SQLRequest(script, tuple(where.values()))

    def select(self, select: Union[List[str], str] = None, FROM: str = None, where: dict = None,
               execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self.__select_stmt__(select=select, table=FROM, where=where, execute=execute, WITH=WITH, **kwargs)

    def select_distinct(self, select: Union[List[str], str] = None, table: str = None, where: dict = None,
                        execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self.__select_stmt__(select=select, table=table, where=where, execute=execute, WITH=WITH, **kwargs)

    def select_all(self, select: Union[List[str], str] = None, table: str = None, where: dict = None,
                   execute: bool = True, WITH: WithType = None, **kwargs) -> Union[SQLRequest, List]:
        return self.__select_stmt__(select=select, table=table, where=where, execute=execute, WITH=WITH, **kwargs)


# ---------------------------------------------------------------------------
# https://www.sitepoint.com/getting-started-sqlite3-basic-commands/
#
#     def delete(self):
#         pass
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
