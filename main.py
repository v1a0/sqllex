from init_types import *
from constants import *
import column_gens as cg
import parsers as parse
import sqlite3
from loguru import logger


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
            sqlite3.connect(self.path)
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
            if isinstance(params, (int, str, float)):
                result += cg.simple(col=col, params=params)

            elif isinstance(params, list):
                result += cg.compound(col=col, params=params)

            elif isinstance(params, dict):
                result += cg.mapped(col=col, params=params)

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
            except Exception as e:
                logger.error(f"{e}\nscript: {script}\nvalues: {values}")

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
                logger.error(e)

    def get_columns(self, table: AnyStr) -> tuple:
        return tuple(map(
            lambda item: item[1],
            self.execute(script=f"PRAGMA table_info({table});")
        ))

    def insert(self, table: AnyStr, *args: Any, **kwargs: Any):
        args, kwargs = parse.args_fix(args=args, kwargs=kwargs)

        if args:
            columns = self.get_columns(table=table)
            columns, args = cg.crop(columns, args)
            unsafe_values = args

        elif kwargs:
            columns = tuple(kwargs.keys())
            unsafe_values = kwargs.values()

        else:
            return

        values = ()
        for val in unsafe_values:
            values += (cg.type_control(val),)

        self.execute(f"INSERT INTO {table} ("
                     f"{', '.join(column for column in columns)}) VALUES ("
                     f"{', '.join('?' * len(values))})", values)

    def select(self):
        pass


db_template: DBTemplateType = {
    "groups": {
        "group_id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, NOT_NULL, DEFAULT, '101'],
    },

    "contact_groups": {
        "contact_id": INTEGER,
        "group_id": INTEGER,

        FOREIGN_KEY: {
            "contact_id": ["contacts", "contact_id"],
            "group_id": ["groups", "group_id"]
        },
    }
}

db = SQL3X(template=db_template)
db.insert("groups", group_id=33, name="MySS")
db.insert("contact_groups", [1233, 2, 5])
db.insert("contact_groups", contact_id=111, group_id={1:2})
# db.select(['contact_id', 'group_id'], from_table='contact_groups', where={'contact_id': 1})
