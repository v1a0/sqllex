from loguru import logger
import sys


class LogFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


def debug_mode(switch: bool = False, mode: str = ''):

    if mode:
        logger.add(sys.stderr, filter=LogFilter(mode), level=0)

    if switch:
        logger.add(sys.stderr, filter=LogFilter("DEBUG"), level=0)
    else:
        logger.add(sys.stderr, filter=LogFilter("INFO"), level=0)


logger.remove(0)
debug_mode(False)

__all__ = [
    'logger',
    'debug_mode'
]
