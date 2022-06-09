"""Декораторы"""
import inspect
import os
import logging
import sys

import log.client_log_config
import log.server_log_config
import traceback


if os.path.split(sys.argv[0])[1] == 'server.py':
    LOGGER = logging.getLogger('server_mess')
elif os.path.split(sys.argv[0])[1].find('client') == 0:
    LOGGER = logging.getLogger('client_mess')


def log(func):
    """Функция-декоратор"""
    def wrapper(*args, **kwargs):
        """Обертка"""
        res = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {os.path.split(sys.argv[0])[1]}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return res
    return wrapper
