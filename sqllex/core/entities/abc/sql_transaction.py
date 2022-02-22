from abc import ABC, abstractmethod
from sqllex.debug import logger
from sqllex.core.entities.abc.sql_database import AbstractDatabase
import sqlite3


class TransactionStatus:
    """
    Class to control transaction status
    (AbstractTransaction.__status: TransactionStatus)

        .is_done
        .is_active
        .mark_as_done()
        .mark_as_active()

    """

    def __init__(self, value: int):
        if value not in (0, 1):
            raise ValueError(f"TransactionStatus value can be 0 or 1, not {value}")

        self.__value = value

    @property
    def is_done(self):
        return self.__value == 1

    @property
    def is_active(self):
        return self.__value == 0

    def mark_as_done(self):
        if self.__value == 0:
            self.__value = 1
        else:
            raise ArithmeticError("Transaction already is not active")

    def mark_as_active(self):
        if self.__value == 1:
            self.__value = 0
        else:
            raise ArithmeticError("Transaction is not finished yet")

    def __str__(self):
        if self.is_done:
            return "Done"
        else:
            return "Active"

    def __repr__(self):
        return f"<TransactionStatus(value={self.__value}, status='{self.__str__()}')>"



class AbstractTransaction(ABC):
    """
    Class for creating transactions. Have to be used inside 'with' statement

        .commit() - commit current transaction
        .rollback() - rollback current transaction
        .begin() - begin new transaction (experimental)

    """

    def __init__(self, db: AbstractDatabase):
        self.__db = db
        self.__status = TransactionStatus(value=0)


    @property
    @abstractmethod
    def __name__(self):
        return "AbstractTransaction"

    @property
    def status(self):
        return self.__status

    def commit(self):
        self.__db.execute("COMMIT;")
        self.status.mark_as_done()

    def rollback(self):
        self.__db.execute("ROLLBACK;")
        self.status.mark_as_done()

    def begin(self):
        if self.status.is_done:
            self.status.mark_as_active()

        try:
            self.__db.execute("BEGIN TRANSACTION;")
        except sqlite3.OperationalError:
            self.__db.execute('COMMIT;')

    def __enter__(self):
        if not self.__db.connection:
            self.__db.connect()

        self.begin()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.status.is_done:
            return

        try:
            self.commit()
            logger.info(f"Transaction committed ({exc_type=}, {exc_val=}, {exc_tb})")

        except Exception as exc:
            self.rollback()
            logger.warning(f"Transaction rolled back: {exc}")


    def __repr__(self):
        return f"<{self.__name__}(status={self.status}, hash={self.__hash__()})>"

