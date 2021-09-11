"""
Middleware for SQLite3x
"""
from sqllex.types import Tuple, AnyStr
from sqllex.debug import logger
import sqlite3


def execute(script: AnyStr, values: Tuple, connection: sqlite3.Connection, path: AnyStr):
    def mw_executor(conn: sqlite3.Connection, script: AnyStr, values: Tuple):
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
            with sqlite3.connect(path) as conn:
                ret_ = mw_executor(conn=conn, script=script, values=values)
                conn.commit()
                return ret_
        else:
            return mw_executor(conn=connection, script=script, values=values)

# here and down below


def executemany(script: AnyStr, values: Tuple, connection: sqlite3.Connection, path: AnyStr):
    def mw_executor(conn: sqlite3.Connection, script: AnyStr, values: Tuple):
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
            with sqlite3.connect(path) as conn:
                ret_ = mw_executor(conn=conn, script=script, values=values)
                conn.commit()
                return ret_
        else:
            return mw_executor(conn=connection, script=script, values=values)


def executescript(script: AnyStr, connection: sqlite3.Connection, path: AnyStr):
    def mw_executor(conn: sqlite3.Connection, script: AnyStr):
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
            with sqlite3.connect(path) as conn:
                ret_ = mw_executor(conn, script)
                conn.commit()
                return ret_
        else:
            return mw_executor(connection, script)
