from sqllex.core.entities.abc.engine import AbstractEngine
from sqllex.core.entities.abc.engine import AbstractConnection


class PostgreSQLxConnection(AbstractConnection):
    class PostgreSQLxCursor:

        def execute(self, script, values=None):
            pass

        def executemany(self, script, values=None):
            pass

        def fetchall(self):
            pass

    def cursor(self) -> PostgreSQLxCursor:
        pass

    def commit(self):
        pass

    def close(self):
        pass


class PostgreSQLxExtensions:
    def new_type(self, *args, **kwargs):
        pass

    def register_type(self, *args, **kwargs):
        pass


class PostgreSQLxEngine(AbstractEngine):
    @property
    def extensions(self) -> PostgreSQLxExtensions:
        return PostgreSQLxExtensions()

    def connect(
            self,
            dbname=None,
            user=None,
            password=None,
            host=None,
            port=None,
            **kwargs
    ) -> PostgreSQLxConnection:
        pass
