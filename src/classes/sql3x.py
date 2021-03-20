from exceptions import TableInfoError, ExecuteError, ArgumentError
from loguru import logger
from constants import *
from types_ import *
import sqlite3
import py2sql


class SQL3X:
    def __init__(self, path: PathType = "sql3x.db", template: DBTemplateType = None):
        """

        :param path: Location of database
        :param mod: Mod, might be readonly or other
        """
        self.path = path
        self.init_db()
        if template:
            self.markup_db(template=template)

    def __str__(self):
        return f"{{SQL3X: path='{self.path}'}}"

    def __bool__(self):
        return self.init_db()

    def init_db(self):
        try:
            self.execute(script="PRAGMA journal_mode=WAL")  # make db little bit faster
            return True
        except Exception as e:
            logger.error(e)

    def markup_db(self, template: DBTemplateType):
        """Need to rename"""
        for (table, columns) in template.items():
            self.create_table(name=table, columns=columns)

    def create_table(self, name: AnyStr, columns: TableType, result: str = ''):
        """
        Create table in bd
        """
        for (col, params) in columns.items():
            result += py2sql.table(col=col, params=params)

        self.execute(
            script=f'CREATE TABLE IF NOT EXISTS "{name}" (\n{result[:-2]}\n);'
        )

    def execute(self, script: AnyStr, values: tuple = None) -> list:
        """

        :return:
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

    def executemany(self, script: AnyStr, load: Union[List, dict]) -> list:
        """
        Sent executemany request to db
        :param script: SQLite script with placeholders: 'INSERT INTO table1 VALUES (?,?,?)'
        :param load: Values for placeholders: [ (1, 'text1', 0.1), (2, 'text2', 0.2) ]

        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
        ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
        ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
        ]
        cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
        """
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:
                print(script, load)
                cur.executemany(script, load)
                conn.commit()
                return cur.fetchall()
            except Exception as e:
                raise e

    def get_columns(self, table: AnyStr) -> tuple:
        columns = self.execute(script=f"PRAGMA table_info({table});")
        if columns:
            return tuple(map(lambda item: item[1], columns))
        else:
            raise TableInfoError

    def insert(self, table: AnyStr, *args: Any, **kwargs: Any) -> List:
        """
        INSERT data into db's table
        :param table: table name for inserting
        :param args: 1'st way set values for insert, if len(args) != number of rows, inserts as much as possible
        if too much values crop off excess, otherwise leave empty
        :param kwargs: 2'st way set values for insert, like: username="Alex", group="None"
        :return: DB answer to or script
        :example:
            SQLite3x.insert(
                "users",
                username="user_1",
                group_id=1
            ) -> INSERT INTO users (username, group_id) VALUES ('user_1', 1);
        """

        if kwargs.get('execute'):
            execute: bool = bool(kwargs.pop('execute'))
        else:
            execute = True

        args, kwargs = insert_ags_fix(args=args, kwargs=kwargs)

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

        script = ''

        script += f"SELECT " \
                  f"{'(' if select[0] != '*' else ''}" \
                  f"{', '.join(sel for sel in select)}" \
                  f"{'(' if select[0] != '*' else ''}" \
                  f" FROM {table} "

        if where:
            script += f"WHERE ({'=?, '.join(wh for wh in where.keys())}=?)"

        script += ';\n'

        if execute:
            return self.execute(script, tuple(where.values()))
        else:
            return [script, tuple(where.values())]
    

def crop(columns: Union[tuple, list], args: Union[tuple, list]) -> tuple:
    """
    Converts columns and arguments to the same length for safe insert
    :param columns:
    :param args:
    :return:
    """
    if args and columns:
        if len(args) != len(columns):
            logger.warning(f"SIZE CROP! Expecting {len(columns)} arguments but {len(args)} were given!")
            _len_ = min(len(args), len(columns))
            return columns[:_len_], args[:_len_]

    return columns, args


def insert_ags_fix(args: Any, kwargs: Any) -> tuple:
    """
    If args = (dict,) :return: (args, kwargs) = (None, dict)
    If args = (list,) :return: (args, kwargs) = (list, None)
    If args = (tuple,) :return: (args, kwargs) = (list, None)
    Otherwise :return: (args, kwargs)
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
    __all__ = [SQL3X]
