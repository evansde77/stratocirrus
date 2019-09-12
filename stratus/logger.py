"""
common package logger

"""

import sys
import logging


_LOGGER = {
    'logger': None,
    'handler': logging.StreamHandler(stream=sys.stdout),
    'formatter': logging.Formatter()
}

def get_logger():
    if _LOGGER['logger'] is not None:
        return _LOGGER['logger']
    logger = logging.getLogger('stratus')
    _LOGGER['handler'].setFormatter(_LOGGER['formatter'])
    _LOGGER['handler'].setLevel(logging.DEBUG)
    logger.addHandler(_LOGGER['handler'])
    logger.setLevel(logging.DEBUG)
    _LOGGER['logger'] = logger
    return _LOGGER['logger']



stratus_logger = get_logger()