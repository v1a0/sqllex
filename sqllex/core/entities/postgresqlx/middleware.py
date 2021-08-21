from sqllex.types import Tuple, AnyStr, Mapping
from sqllex.debug import logger
from psycopg2.extensions import connection



def execute(script: AnyStr, values: Tuple, connection: connection):
    def mw_executor(conn: connection, script: AnyStr, values: Tuple):
        cur = conn.cursor()

        try:
            if values:
                cur.execute(script, values)
            else:
                cur.execute(script)

            return cur.fetchall()

        except Exception as error:
            raise error


    if script:  # it's necessary
        script = script.strip()

        logger.debug(f"\n {script}\n {values if values else ''}\n")

        # If connection does not exist create temporary
        if not connection:
            raise ConnectionError("Can't execute script, no connection to database")
        else:
            return mw_executor(conn=connection, script=script, values=values)

# here and down below


def executemany(script: AnyStr, values: Tuple, connection: connection):
    def mw_executor(conn: connection, script: AnyStr, values: Tuple):
        cur = conn.cursor()

        try:
            cur.executemany(script, values)
            return cur.fetchall()

        except Exception as error:
            raise error

    if script:  # it's necessary
        script = script.strip()

        logger.debug(f"\n {script}\n {values if values else ''}\n")

        if not connection:
            raise ConnectionError("Can't execute script, no connection to database")
        else:
            return mw_executor(conn=connection, script=script, values=values)


def executescript(script: AnyStr, connection: connection):
    def mw_executor(conn: connection, script: AnyStr):
        cur = conn.cursor()

        try:
            cur.executescript(script)
            return cur.fetchall()

        except Exception as error:
            raise error

    if script:  # it's necessary
        script = script.strip()

        logger.debug(f"\n {script}\n")

        if not connection:
            raise ConnectionError("Can't execute script, no connection to database")
        else:
            return mw_executor(connection, script)
