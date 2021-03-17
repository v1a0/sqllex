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
        for (name, columns) in template.items():
            self.create_table(name=name, columns=columns)

    def create_table(self, name: AnyStr, columns: TableType):
        """
        Create table in bd
        """

        _columns = ''

        for (column, params) in columns.items():
            if isinstance(params, (int, str)):
                _columns += f"{column} {stc(params)}" + ',\n'
            elif isinstance(params, list):
                if "FOREIGN KEY" not in params:
                    _columns += f"{column}"
                    for param in params:
                        _columns += f' {stc(param)}'
                else:
                    _columns += f"FOREIGN KEY ({params[1]}) REFERENCES {column} ({params[1]})"
                    for param in params[2:]:
                        _columns += f" {param}"
                _columns += ',\n'

            else:
                raise TypeError

        script = f'CREATE TABLE IF NOT EXISTS "{name}" (\n{_columns[:-2]}\n);'
        print(script)

    def insert(self, table: str, mod: ReadType, *args: InsertType, **kwargs: InsertType):
        if mod is ReadOnlyMode:
            return False

        pass


my_template: TemplateType = {
    "my_table": {
        "id": [INTEGER, PRIMARY_KEY, UNIQUE],
        "name": [TEXT, DEFAULT, '101'],
        "age": INTEGER,
        "super_id": [FOREIGN_KEY, 'contacts'],
        "mega_id":  [FOREIGN_KEY, 'contacts', "ON DELETE CASCADE ON UPDATE NO ACTION"]
    }
}

db = SQL3X(template=my_template)
# print(db)
