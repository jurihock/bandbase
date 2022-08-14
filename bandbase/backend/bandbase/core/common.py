import click
import functools
import logging
import os

from logging import Formatter, LoggerAdapter
from logging.handlers import RotatingFileHandler
from pydantic import BaseSettings

import bandbase.defaults


class Config(BaseSettings):

    title: str = 'Bandbase Backend'
    description: str = ''
    version: str = '2.0'

    def __init__(self, file=bandbase.defaults.config):

        if file:

            click.secho(f'Init custom configs from {file}')

        else:

            click.secho('Init default configs')

        super().__init__(_env_file=file)

    class Config:

        env_prefix: str = 'BANDBASE_'


@functools.lru_cache()
def config():
    return Config()


# filter log entries by explicit logging level,
# e.g. logging.WARNING or logging.ERROR
class ExplicitLoggingFilter:

    def __init__(self, level):
        self.__level = level

    def filter(self, record):
        return record.levelno == self.__level


class Logger(LoggerAdapter):

    def __init__(self, directory=bandbase.defaults.logs):

        super().__init__(logger=logging.getLogger('bandbase'), extra={})

        click.secho(f'Init logs in {directory}')

        MB = 1024 * 1024

        formatter = Formatter('%(asctime)s %(levelname)s %(filename)s [%(funcName)s:%(lineno)d] %(message)s')

        loggers = \
        {
            'bandbase': logging.getLogger('bandbase'),
            'sqlalchemy': logging.getLogger('sqlalchemy'),
            'uvicorn': logging.getLogger('uvicorn'),
        }

        args = { 'maxBytes': 1*MB, 'backupCount': 10 }

        handlers = \
        {
            'bandbase.main': RotatingFileHandler(os.path.join(directory, 'bandbase.main.log'), **args),
            'bandbase.warning': RotatingFileHandler(os.path.join(directory, 'bandbase.warning.log'), **args),
            'bandbase.error': RotatingFileHandler(os.path.join(directory, 'bandbase.error.log'), **args),
            'sqlalchemy': RotatingFileHandler(os.path.join(directory, 'sqlalchemy.log'), **args),
            'uvicorn': RotatingFileHandler(os.path.join(directory, 'uvicorn.log'), **args),
        }

        for key in handlers.keys():
            handlers[key].setFormatter(formatter)

        handlers['bandbase.main'].setLevel(logging.INFO)
        handlers['bandbase.warning'].setLevel(logging.WARNING)
        handlers['bandbase.warning'].addFilter(ExplicitLoggingFilter(logging.WARNING))
        handlers['bandbase.error'].setLevel(logging.ERROR)
        handlers['sqlalchemy'].setLevel(logging.WARNING)
        handlers['uvicorn'].setLevel(logging.INFO)

        for key in handlers.keys():

            if 'bandbase' in key:
                loggers['bandbase'].addHandler(handlers[key])

            if 'sqlalchemy' in key:
                loggers['sqlalchemy'].addHandler(handlers[key])

            if 'uvicorn' in key:
                loggers['uvicorn'].addHandler(handlers[key])

        for key in loggers.keys():
            loggers[key].setLevel(logging.INFO)


@functools.lru_cache()
def logger():
    return Logger()
