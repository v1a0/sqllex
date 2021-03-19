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
        print(script, values if values else '', '\n')
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
                logger.error(e)

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

    def get_columns_list(self, table: AnyStr) -> list:
        return list(map(
            lambda item: item[1],
            self.execute(script=f"PRAGMA table_info({table});")
        ))

    def insert(self, table: AnyStr, *args: InsertArgs, **kwargs: InsertKwargs):
        args, kwargs = parse.args_fix(args=args, kwargs=kwargs)

        if args:
            # columns = self.get_columns_list(table=table)
            # values = args
            #
            # if len(values) != len(columns):
            #     logger.warning(f"SIZE CROP! Expecting {len(columns)} arguments but {len(values)} were given!")
            #     crop = min(len(values), len(columns))
            #     columns, values = columns[:crop], values[:crop]

            columns, values = cg.crop_size(
                columns=self.get_columns_list(table=table),  # list of columns of table
                values=parse.args2list(args)                 # parsing args
            )

        elif kwargs:
            columns, values = parse.kwargs2lists(kwargs)  # split dict on 2 lists [keys] and [values]

        else:
            return

        # self.execute(f"INSERT INTO {table} ("
        #             f"{', '.join(map(str, columns))}) VALUES ("
        #             f"{', '.join(map(cg.qtc, values))})", )

        self.execute(f"INSERT INTO {table} ("
                     f"{', '.join(map(str, columns))}) VALUES ("
                     f"{', '.join('?' * len(values))})", tuple(cg.qtc_foreach_in(values)))

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
# db.insert("groups", group_id=33, name="MySS")
# db.insert("contact_groups", [1233, 2, 5])
db.insert("contact_groups", contact_id=111, group_id={1:2})
# db.select(['contact_id', 'group_id'], from_table='contact_groups', where={'contact_id': 1})
