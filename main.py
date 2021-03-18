from init_types import *
from constants import *
import column_gens as cg
import sqlite3


class SQL3X:
    def __init__(self, path: PathType = "sql3x.db", mod: ReadType = None, template: DBTemplateType = None):
        """

        :param path: Location of database
        :param mod: Mod, might be readonly or other
        """
        self.path = path
        self.mod = mod
        self.init_db()
        if template:
            self.markup_db(template=template)

    def __str__(self):
        return f"{{SQL3X: path='{self.path}'}}"

    def __bool__(self):
        """Is db available"""
        return True

    def init_db(self):
        try:
            sqlite3.connect(self.path)
        except Exception as e:
            raise e

    def markup_db(self, template: DBTemplateType):
        """Need to rename"""
        for (table, columns) in template.items():
            self.create_table(name=table, columns=columns)

    def create_table(self, name: AnyStr, columns: TableType, result: str = ''):
        """
        Create table in bd
        """
        for (col, params) in columns.items():
            if isinstance(params, (int, str)):
                result += cg.simple(col=col, params=params)

            elif isinstance(params, list):
                result += cg.compound(col=col, params=params)

            elif isinstance(params, dict):
                result += cg.mapped(col=col, params=params)

        self.execute(
            script=f'CREATE TABLE IF NOT EXISTS "{name}" (\n{result[:-2]}\n);'
        )

    def execute(self, script: AnyStr):
        """
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
        cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
        :return:
        """
        print(script, '\n')
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:
                cur.execute(script)
                conn.commit()
            except Exception as error:
                raise error

    def executemany(self, script: AnyStr, load: Union[List, Mapping]):
        """
        Sent executemany request to db
        :param script: SQLite script with placeholders: 'INSERT INTO table1 VALUES (?,?,?)'
        :param load: Values for placeholders: [ (1, 'text1', 0.1), (2, 'text2', 0.2) ]
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            try:
                cursor.executemany(script, load)
                conn.commit()
            except Exception as error:
                raise error

    def insert(self, table: str, mod: ReadType, *args: InsertType, **kwargs: InsertType):
        if mod is ReadOnlyMode:
            return False

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
