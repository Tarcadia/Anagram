
# -*- coding: UTF-8 -*-


import logging
import logging.handlers

from ._consts import ROOT_CWD
from ._consts import PATH_DOT_ANAGRAM
from ._consts import PATH_LOG


_LOG_FILE = ROOT_CWD / PATH_DOT_ANAGRAM / PATH_LOG

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.NOTSET)

_LOG_FORMATTER_FILE = logging.Formatter(fmt="[%(asctime)s][%(levelname)s][%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
_LOG_FORMATTER_CONSOLE = logging.Formatter(fmt="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%H:%M:%S")

_LOG_HANDLER_FILE = logging.handlers.TimedRotatingFileHandler(_LOG_FILE)
_LOG_HANDLER_FILE.setFormatter(_LOG_FORMATTER_FILE)
_LOG_HANDLER_FILE.setLevel(logging.NOTSET)

_LOG_HANDLER_CONSOLE = logging.StreamHandler()
_LOG_HANDLER_CONSOLE.setFormatter(_LOG_FORMATTER_CONSOLE)


def logging_set(file_enable=None, console_enable=None, console_level=None):
    if file_enable is True:
        _LOGGER.addHandler(_LOG_HANDLER_FILE)
    elif file_enable is False:
        _LOGGER.removeHandler(_LOG_HANDLER_FILE)
    
    if console_enable is True:
        _LOGGER.addHandler(_LOG_HANDLER_CONSOLE)
    elif console_enable is False:
        _LOGGER.removeHandler(_LOG_HANDLER_CONSOLE)
    
    if not console_level is None:
        _LOG_HANDLER_CONSOLE.setLevel(console_level)

