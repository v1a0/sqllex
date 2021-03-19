from exceptions import TableInfoError, ExecuteError
from parsers.args_ import argfix
from other.crop_ import crop
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
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
        cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
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

    def executemany(self, script: AnyStr, load: Union[List, Mapping]) -> list:
        """
        Sent executemany request to db
        :param script: SQLite script with placeholders: 'INSERT INTO table1 VALUES (?,?,?)'
        :param load: Values for placeholders: [ (1, 'text1', 0.1), (2, 'text2', 0.2) ]
        """
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:
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

    def insert(self, table: AnyStr, *args: Any, **kwargs: Any):
        args, kwargs = argfix(args=args, kwargs=kwargs)

        if args:
            columns = self.get_columns(table=table)
            columns, args = crop(columns, args)
            unsafe_values = args

        elif kwargs:
            columns = tuple(kwargs.keys())
            unsafe_values = kwargs.values()

        else:
            return

        values = ()
        for val in unsafe_values:
            values += (py2sql.quote(val),)

        self.execute(f"INSERT INTO {table} ("
                     f"{', '.join(column for column in columns)}) VALUES ("
                     f"{', '.join('?' * len(values))})", values)

    def select(self):
        pass


if __name__ == "__main__":
    __all__ = [SQL3X]

