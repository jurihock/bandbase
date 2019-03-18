__logger__ = None

def setup(app):

    import click
    import os
    import logging

    from logging import Formatter
    from logging.handlers import RotatingFileHandler

    # Filter log entries by explicit logging level, e.g. logging.WARNING
    class ExplicitLoggingFilter(object):
        def __init__(self, level):
            self.__level = level
        def filter(self, record):
            return record.levelno == self.__level

    click.secho(' * Setting up logs {0}'.format(app.config['LOGS']))

    MB = 1024*1024

    log_formatter = Formatter('%(asctime)s %(levelname)s %(filename)s [%(funcName)s:%(lineno)d] %(message)s')
    lgn_formatter = Formatter('%(asctime)s %(message)s')

    log_inf = RotatingFileHandler(os.path.join(app.config['LOGS'], 'main.log'),    maxBytes=1*MB, backupCount=10)
    log_wrn = RotatingFileHandler(os.path.join(app.config['LOGS'], 'warning.log'), maxBytes=1*MB, backupCount=10)
    log_err = RotatingFileHandler(os.path.join(app.config['LOGS'], 'error.log'),   maxBytes=1*MB, backupCount=10)
    log_dbg = RotatingFileHandler(os.path.join(app.config['LOGS'], 'debug.log'),   maxBytes=1*MB, backupCount=10)
    log_sql = RotatingFileHandler(os.path.join(app.config['LOGS'], 'sql.log'),     maxBytes=1*MB, backupCount=10)
    log_lgn = RotatingFileHandler(os.path.join(app.config['LOGS'], 'login.log'),   maxBytes=1*MB, backupCount=10)

    log_inf.setFormatter(log_formatter)
    log_wrn.setFormatter(log_formatter)
    log_err.setFormatter(log_formatter)
    log_dbg.setFormatter(log_formatter)
    log_sql.setFormatter(log_formatter)
    log_lgn.setFormatter(lgn_formatter)

    log_inf.setLevel(logging.INFO)
    log_wrn.setLevel(logging.WARNING)
    log_err.setLevel(logging.ERROR)
    log_dbg.setLevel(logging.DEBUG)
    log_sql.setLevel(logging.WARNING)
    log_lgn.setLevel(logging.INFO)

    log_wrn.addFilter(ExplicitLoggingFilter(logging.WARNING))
    log_dbg.addFilter(ExplicitLoggingFilter(logging.DEBUG))

    # Setup default application logger
    app.logger.addHandler(log_inf)
    app.logger.addHandler(log_wrn)
    app.logger.addHandler(log_err)
    app.logger.addHandler(log_dbg)

    # Setup additional SQLAlchemy logger
    sql_logger = logging.getLogger('sqlalchemy')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(log_sql)

    # Setup the login logger
    lgn_logger = logging.getLogger('bandbase.login')
    lgn_logger.setLevel(logging.INFO)
    lgn_logger.addHandler(log_lgn)

    global __logger__
    __logger__ = app.logger

def debug(message, *args, **kwargs):

    __logger__.debug(message, *args, **kwargs)

def info(message, *args, **kwargs):

    __logger__.info(message, *args, **kwargs)

def warning(message, *args, **kwargs):

    __logger__.warning(message, *args, **kwargs)

def error(message, *args, **kwargs):

    __logger__.error(message, *args, **kwargs)

def exception(message, *args, **kwargs):

    __logger__.exception(message, *args, **kwargs)

def login(ip, agent, secret, ok):

    import logging

    message = 'LOGIN  OK  IP {0} AGENT {1}'.format(ip, agent) if ok else \
              'LOGIN  NOK IP {0} AGENT {1} SECRET \"{2}\"'.format(ip, agent, secret or '')

    logging.getLogger('bandbase.login').info(message)

def logout(ip, agent):

    import logging

    message = 'LOGOUT     IP {0} AGENT {1}'.format(ip, agent)

    logging.getLogger('bandbase.login').info(message)
