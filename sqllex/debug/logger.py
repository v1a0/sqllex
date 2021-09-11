"""
SqllexLogger for logging
"""
from loguru import logger as __logger
from sys import stderr


class SqllexLogger:
    """
    0 - debug
    1 - info
    2 - ?
    3 - warning
    4 - error

    """
    def __init__(self, logger, level=3):
        self._level = level
        self.logger = logger

    def warning(self, message: str, *args, **kwargs):
        if self._level <= 3:
            self.logger.warning(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        if self._level <= 1:
            self.logger.info(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        if self._level == 0:
            self.logger.debug(message, *args, **kwargs)

    def level(self, level: int, log_file="sqllex.log"):
        self._level = level

        if self._level == 0:
            self.logger.remove(0)
            self.logger.add(log_file, level=0, rotation="10Mb", compression="zip")
            self.logger.add(stderr, level=0)

    def stop(self):
        self.logger.stop()


def debug_mode(switch: bool = False, log_file: str = "sqllex.log", mode: str = ''):
    """
    Set logger on/off

    switch : bool
        Turn on debug mode
    log_file : str
        Path to log file
    mode : str
        Advanced mode options
    """

    if mode == "DEBUG":
        logger.level(0)
    elif mode == "INFO":
        logger.level(1)
    elif mode == "?":
        logger.level(2)
    elif mode == "WARNING":
        logger.level(3)
    elif mode == "ERROR":
        logger.level(4)

    if switch:
        logger.level(level=0, log_file=log_file)
    else:
        logger.level(4)


logger = SqllexLogger(logger=__logger, level=3)


__all__ = [
    'logger',
    'debug_mode'
]
