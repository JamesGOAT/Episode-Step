from datetime import timedelta
from typing import Optional
import sys
import time
import logging


class LogFormatter(logging.Formatter):
    def __init__(self):
        self.start_time = time.time()

    def format(self, record):

        # define prefix
        # record.pathname / record.filename / record.lineno
        curr_date = time.strftime("%y-%m-%d %H:%M:%S")
        delta = timedelta(seconds=round(record.created - self.start_time))
        prefix = f"{record.levelname:<7} {curr_date} - {delta} - "

        # logged content
        content = record.getMessage()
        content = content.replace("\n", "\n" + " " * len(prefix))

        return f"{prefix}{content}"


def initialize_logger(filepath: Optional[str]) -> logging.Logger:

    # log everything
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    # stdout: everything
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.NOTSET)
    stdout_handler.setFormatter(LogFormatter())

    # stderr: warnings / errors and above
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(LogFormatter())

    # set stream handlers
    logger.handlers.clear()  # TODO: remove once fixed in xformers
    assert len(logger.handlers) == 0, logger.handlers
    logger.handlers.append(stdout_handler)
    logger.handlers.append(stderr_handler)

    # file handler
    if filepath is not None:
        add_logger_file_handler(filepath)

    return logger


def add_logger_file_handler(filepath: str):

    # build file handler
    file_handler = logging.FileHandler(filepath, "a")
    file_handler.setLevel(logging.NOTSET)
    file_handler.setFormatter(LogFormatter())

    # update logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)