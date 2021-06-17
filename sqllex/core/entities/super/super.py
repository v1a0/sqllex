"""
Not finished yet

Parent class for all 
"""

from sqllex.types import *


class Table:
    def __init__(self, db, name: AnyStr):
        self.db: Database = db
        self.name: AnyStr = name


class Database:
    """
    Parent class for all database-classes

    """

    def __init__(self, template = None):
        """
        Initialization

        Parameters
        ----------
        template : DBTemplateType
            template of database structure (DBTemplateType)

        """
        self.tables = self._get_tables_()
        self.tables_names = self._get_tables_names_()

        if template:
            self.markup(template=template)

    def __getitem__(self, key) -> Table:
        # To call method down below is necessary,
        # otherwise it might fall in case of multiple DB objects
        self._update_instance_variables_()

        if key not in self.tables_names:
            raise KeyError(key, "No such table in database",
                           f"Available tables: {self.tables_names}")

        return Table(db=self, name=key)

    def _update_instance_variables_(self):
        pass

    def _get_tables_(self) -> Generator[Table, None, None]:
        """
        Generator of tables list

        Yield
        ----------
        SQLite3xTable
            Tables list

        """

        # Code down below commented because I guess it's better to see all tables
        # even Internal SQLite tables. Might be changed later
        #
        # if "sqlite_sequence" in table_names:
        #     table_names.remove("sqlite_sequence")

        for tab_name in self.tables_names:
            yield self.__getitem__(tab_name)
            # tables.append(self.__getitem__(tab_name))

        # line down below it is necessary for possibility to call self.tables unlimited times
        # make it never end, because in the end of generation it'll be overridden
        self.tables = self._get_tables_()

    def _get_tables_names_(self) -> List[str]:
        """
        Get list of tables names from database

        Returns
        ----------
        List[str]
            list of tables names

        """
        pass

    @__update_constants__
    def markup(
            self,
            template
    ):
        """
        Mark up table structure from template

        Parameters
        ----------
        template : DBTemplateType
            Template of database structure (DBTemplateType-like)

        """

        for (table_name, columns) in template.items():
            self.create_table(
                name=table_name,
                columns=columns,
                IF_NOT_EXIST=True
            )


class XXX(Database):
    def __init__(self):
        super().__init__()
