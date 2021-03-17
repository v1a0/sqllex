from init_types import *
from constants import *
import sqlite3


def stc(param: Any):
    """
    String control
    :param param:
    :return:
    """
    if param not in CONSTANTS and type(param) == str:
        return f'"{param}"'
    else:
        return f'{param}'



class SQL3X:
    def __init__(self, path: PathType = "sql3x.db", mod: ReadType = None, template: TemplateType = None):
        """

        :param path: Location of database
        :param mod: Mod, might be readonly or other
        """
        self.path = path
        self.mod = mod
        self.init_db()
        if template:
            self.init_template(template)

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

    def init_template(self, template: TemplateType):
        """Need to rename"""
        for (table, columns) in template.items():
            self.create_table(name=table, columns=columns)

    def create_table(self, name: AnyStr, columns: TableType):
        """
        Create table in bd
        """

        _columns = ''

        for (col, params) in columns.items():
            if isinstance(params, (int, str)):
                _columns += f"{col} {stc(params)}" + ',\n'

            elif isinstance(params, list):
                for param in params:
                    _columns += f' {stc(param)}'

                _columns = f"{col}{_columns},\n"

            elif isinstance(params, dict):
                if col == FOREIGN_KEY:
                    for (key, refs) in params.items():
                        _columns += f"FOREIGN KEY ({key}) REFERENCES {refs[0]} ({refs[1]})"
                        for ref in refs[2:]:
                            _columns += f" {ref}"
                        _columns += ',\n'

            else:
                raise TypeError

        script = f'CREATE TABLE IF NOT EXISTS "{name}" (\n{_columns[:-2]}\n);'
        self.execute(script)

    def execute(self, script: AnyStr):
        """
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
        cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
        :return:
        """
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            try:
                cur.execute(script)
                conn.commit()
            except Exception as error:
                raise error


    def insert(self, table: str, mod: ReadType, *args: InsertType, **kwargs: InsertType):
        if mod is ReadOnlyMode:
            return False

        pass


my_template: TemplateType = {
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

db = SQL3X(template=my_template)
# print(db)
