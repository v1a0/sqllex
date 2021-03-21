from sqllex.exceptions import TableInfoError, ExecuteError, ArgumentError
from loguru import logger
from sqllex.constants import *
from sqllex.types_ import *
import sqlite3


class SQLite3x:
    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """
        SQLite3x
        :param path: Location of database
        :param template: template of DB structure
        """
        self.path = path
        self.journal_mode(mode="WAL")
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

    def pragma(self, pram: str):
        try:
            self.execute(script=f"PRAGMA {pram}")  # make db little bit faster
            return True
        except Exception as e:
            logger.error(e)

    def foreign_keys(self, mode: Literal["ON", "OFF"]):
        self.pragma(f"foreign_keys={mode}")

    def journal_mode(self, mode: Literal["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]):
        self.pragma(f"journal_mode={mode}")

    def __markup__(self, template: DBTemplateType):
        """Need to rename"""
        for (table, columns) in template.items():
            self.create_table(name=table, columns=columns)

    def create_table(self, name: AnyStr, columns: TableType, safe: bool = True):
        """
        Create table in db
        :param name: table name
        :param columns: table's columns
        :param safe: Convert not supported types in columns.values() to string, like [1, 2, 3] -> "[1, 2, 3]"
        :return:
        """
        result: str = ''

        for (col, params) in columns.items():
            result += table(col=col, params=params, safe=safe)

        self.execute(
            script=f'CREATE TABLE IF NOT EXISTS "{name}" (\n{result[:-2]}\n);'
        )

    def execute(self, script: AnyStr, values: tuple = None) -> list:
        """
        Execute SQL script
        :param script: SQLite script with placeholders: 'INSERT INTO table1 VALUES (?,?,?)'
        :param values: Values for placeholders: ( (1, 'text1', 0.1), (2, 'text2', 0.2) )
        :return: DB answer
        """
        # print(script, values if values else '', '\n')
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:
                if values:
                    cur.execute(script, values)
                else:
                    cur.execute(script)
                conn.commit()

                return cur.fetchall()
            except Exception as error:
                raise ExecuteError(error=error, script=script, values=values)

    def executemany(self, script: AnyStr, values: tuple) -> list:
        """
        Sent executemany request to db
        :param script: SQLite script with placeholders: 'INSERT INTO table1 VALUES (?,?,?)'
        :param values: Values for placeholders: ( (1, 'text1', 0.1), (2, 'text2', 0.2) )
        :return: DB answer
        """
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:

                cur.executemany(script, values)
                conn.commit()
                return cur.fetchall()
            except Exception as e:
                raise e

    def get_columns(self, table: AnyStr) -> tuple:
        """
        Get list of table columns
        :param table: table where from you want to get columns
        :return: [ (cid, name, type, notnull, default val, pk), ... ]
        """
        columns = self.execute(script=f"PRAGMA table_info({table});")
        if columns:
            return tuple(map(lambda item: item[1], columns))
        else:
            raise TableInfoError

    def insert(self, table: AnyStr, *args: Any, **kwargs: Any) -> List:
        """
        INSERT data into db's table
        :param table: table name for inserting
        :param args: 1'st way set values for insert, if len(values) != number of rows, inserts as much as possible
        if too much values crop off excess, otherwise leave empty
        :param kwargs: 2'st way set values for insert, like: username="Alex", group="None"
        :return: DB answer or script
        :example:
            SQLite3x.insert(
                "users",
                username="user_1",
                group_id=1
            ) -> INSERT INTO users (username, group_id) VALUES ('user_1', 1);
        """

        if 'execute' in kwargs.keys():
            execute: bool = bool(kwargs.pop('execute'))
        else:
            execute = True

        args, kwargs = insert_args_fix(args=args, kwargs=kwargs)

        if args:
            columns = self.get_columns(table=table)
            columns, args = crop(columns, args)
            values = tuple(args)

        elif kwargs:
            columns = tuple(kwargs.keys())
            values = tuple(kwargs.values())

        else:
            raise ArgumentError(args_kwargs="Unset", error="No data to insert")

        script = f"INSERT INTO {table} (" + \
                 f"{', '.join(column for column in columns)}) VALUES (" + \
                 f"{', '.join('?' * len(values))})"

        if execute:
            self.execute(script, values)
        else:
            return [script, values]

    def insertmany(self, table: AnyStr, *args: Union[list[list], list[tuple], tuple[list], tuple[tuple], list, tuple],
                   **kwargs: Any):
        """
        INSERT many data into db's table
        The same as regular insert but for lists of inserts
        :param table: table name for inserting
        :param args: 1'st way set values for insert, awaiting list [[a, b, c], [d, e, f]]
        :param kwargs: 2'st way set values for insert, like: username=["Alex", "Bob"], group=[1, 2]
        :return: None
        :example:
            db.insertmany(
                table="users",
                [("Alex", 1), ("Bob", 2), ("Anon", 0)]
            ) -> INSERT INTO users (username, group_id) VALUES (?, ?);
        """
        if args:
            values = list(map(lambda arg: list(arg), args))   # make values list[list] (yes it's necessary)

            if len(values) == 1 and isinstance(values[0], list):
                values = values[0]

            max_l = max(map(lambda arg: len(arg), values))   # max len of arg in values
            temp_ = [0 for _ in range(max_l)]                 # example values [] for script
            script = self.insert(table, temp_, execute=False)
            _len = len(script[1])

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

            script = self.insert(table, temp_, execute=False)
            max_l = max(map(lambda val: len(val), args))   # max len of arg in values

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
        self.executemany(script[0], values)

    def select(self, select: Union[List[str], str] = None, table: str = None,
               where: dict = None, execute: bool = True, **kwargs) -> List:
        """
        SELECT columns from (one) table
        :param select: columns to select, have shadow name in kwargs 'columns'. Value '*' by default
        :param table: table for selection, have shadow name in kwargs 'from_table'
        :param where: optional parameter for conditions, example: {'name': 'Alex', 'group': 2}
        :param kwargs: shadow names holder (columns, from_table)
        :param execute: execute script and return db's answer (True) or return script (False)
        :return: DB answer to or script
        :example:
            SQLite3x().select(
                select=['id', 'about'],
                table='users',
                where={name: 'Alex', group: 2}
                ) -> SELECT (id, about) FROM users WHERE (name='Alex', group=2)
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

        script += ';\n'

        if execute:
            return self.execute(script, tuple(where.values()))
        else:
            return [script, tuple(where.values())]


def table(col: AnyStr, params: Any, safe: bool = True):
    if isinstance(params, list):
        if safe:
            return f"{col} {' '.join(quote(param) for param in params)},\n"
        else:
            return f"{col} {' '.join(param for param in params)},\n"

    elif isinstance(params, str):
        if safe:
            return f"{col} {quote(params)}" + ',\n'
        else:
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
    :param columns: List of columns in some table
    :param values: Values for insert to some table
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


def insert_args_fix(args: Any, kwargs: Any) -> tuple:
    """
    If values = (dict,) :return: (values, kwargs) = (None, dict)
    If values = (list,) :return: (values, kwargs) = (tuple(list), None)
    If values = (tuple,) :return: (values, kwargs) = (list, None)
    Otherwise :return: (values, kwargs)
    """

    if len(args) == 1:
        if isinstance(args[0], dict):
            return None, args[0]
        if isinstance(args[0], list):
            return tuple(args[0]), None
        if isinstance(args[0], tuple):
            return args[0], None
        else:
            return args, None

    else:
        return args, kwargs


if __name__ == "__main__":
    __all__ = [SQLite3x]
