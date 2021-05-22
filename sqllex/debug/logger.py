from loguru import logger
import sys


class LogFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


def debug_mode(switch: bool = False, log_file: str = "", mode: str = '', ):
    """
    Set logger on/off
    """

    if not mode:
        if switch:
            mode = "DEBUG"
        else:
            mode = "INFO"

    if log_file:
        logger.add(log_file, filter=LogFilter(mode), level=0, rotation="10Mb", compression="zip")

    logger.add(sys.stderr, filter=LogFilter(mode), level=0)


logger.remove(0)
debug_mode(False)

__all__ = [
    'logger',
    'debug_mode'
]
