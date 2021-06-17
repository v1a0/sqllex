from sqllex.types import Tuple, Mapping, SQLStatement
from sqllex.debug import logger
import sqlite3


def execute(func: callable):
    """
    Decorator for execute SQLStatement
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def execute_wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                if stmt.request.values:
                    cur.execute(stmt.request.script, stmt.request.values)
                else:
                    cur.execute(stmt.request.script)

                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)

        if stmt:    # it's necessary
            stmt.request.script = stmt.request.script.strip()

            if not execute:
                return stmt

            logger.debug(
                f"\n"
                f"{stmt.request.script.strip()}\n"
                f"{stmt.request.values if stmt.request.values else ''}"
                f"\n"
            )

            # If connection does not exist
            if not stmt.connection:
                with sqlite3.connect(stmt.path) as conn:
                    ret_ = executor(conn, stmt)
                    conn.commit()
                    return ret_
            else:
                return executor(stmt.connection, stmt)

    return execute_wrapper


def executemany(func: callable):
    """
    Decorator for execute SQLStatement with multiple values
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                cur.executemany(stmt.request.script, stmt.request.values)
                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)

        if stmt:    # it's necessary
            stmt.request.script = stmt.request.script.strip()

            if not execute:
                return stmt

            logger.debug(
                f"\n"
                f"{stmt.request.script.strip()}\n"
                f"{stmt.request.values if stmt.request.values else ''}"
                f"\n"
            )

            if not stmt.connection:
                with sqlite3.connect(stmt.path) as conn:
                    ret_ = executor(conn, stmt)
                    conn.commit()
                    return ret_
            else:
                return executor(stmt.connection, stmt)

    return wrapper


def executescript(func: callable):
    """
    Decorator for execute SQLStatement with script only (without values)
    catching :param execute: boolean argument in kwargs of method, True by default

    If it has, executing script otherwise returning SQLStatement

    Parameters
    ----------
    func : callable
        SQLite3x method

    Returns
    ----------
    callable
        Database answer (if execute True) or SQLStatement (if execute False) or None

    """

    def wrapper(*args: Tuple, **kwargs: Mapping):
        def executor(conn: sqlite3.Connection, stmt: SQLStatement):
            cur = conn.cursor()

            try:
                cur.executescript(stmt.request.script)
                return cur.fetchall()

            except Exception as error:
                raise error

        if "execute" in kwargs.keys():
            execute = bool(kwargs.pop("execute"))
        else:
            execute = True

        stmt: SQLStatement = func(*args, **kwargs)

        if stmt:    # it's necessary
            stmt.request.script = stmt.request.script.strip()

            if not execute:
                return stmt

            logger.debug(
                f"\n"
                f"{stmt.request.script.strip()}\n"
                f"{stmt.request.values if stmt.request.values else ''}"
                f"\n"
            )

            if not stmt.connection:
                with sqlite3.connect(stmt.path) as conn:
                    ret_ = executor(conn, stmt)
                    conn.commit()
                    return ret_
            else:
                return executor(stmt.connection, stmt)

    return wrapper