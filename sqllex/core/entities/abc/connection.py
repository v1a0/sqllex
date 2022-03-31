from abc import ABC, abstractmethod


class AbstractConnection(ABC):

    class AbstractCursor(ABC):

        @abstractmethod
        def execute(self, script, values=None):
            """
            script:
                INSERT (?, ?, ?) INTO 'table_name'
            values:
                (1, 2, 3)
            """
            pass

        @abstractmethod
        def executemany(self, script, values=None):
            """
            script:
                INSERT (?, ?, ?) INTO 'table_name'
            values:
                ((1, 2, 3), (2, 3, 4), (3, 4, 5))
           """
            pass

        # @abstractmethod
        # def executescript(self, script, values=None):
        #     """
        #     script:
        #         INSERT (?, ?, ?) INTO 'table_name';
        #         SELECT * FROM 'table_name' WHERE col=?
        #     values:
        #         (
        #             1, 2, 3,
        #             'Column_value'
        #         )
        #     """
        #     pass

        @abstractmethod
        def fetchall(self):
            pass

    @abstractmethod
    def cursor(self) -> AbstractCursor:
        pass
