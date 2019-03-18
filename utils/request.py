import flask
import datetime

def ip():    return flask.request.remote_addr
def agent(): return flask.request.user_agent.string

def isget():  return flask.request.method == 'GET'
def ispost(): return flask.request.method == 'POST'

def has(key):

    from builtins import bool as __bool__

    return __bool__(flask.request.values.get(key, '').strip())

def value(key):

    return flask.request.values.get(key)

def str(key, default=None, format='{0}'):

    return format.format(value(key)) \
        if has(key) else default

def bool(key, default=False):

    return True if has(key) else default

def int(key, default=None):

    from builtins import int as __int__

    return __int__(value(key)) if has(key) else default

def float(key, default=None):

    from builtins import float as __float__

    return __float__(value(key).replace(',', '.', 1)) if has(key) else default

def date(key, default=None):

    from builtins import int as __int__

    if not has(key): return default

    values = value(key).split('.', 2)

    if len(values) < 2:

        raise ValueError('Invalid date value "{0}", expected "{1}"!'
                         .format(value(key), 'DD.MM.YYYY, DD.MM.YYYY or just DD.MM.'))

    day   = __int__(values[0])
    month = __int__(values[1])
    year  = __int__(values[2]) \
            if len(values) > 2 and values[2] \
            else datetime.datetime.now().year

    if year < 1000: year += 2000

    return datetime.date(year, month, day)

def time(key, default=None):

    from builtins import int as __int__

    if not has(key): return default

    values = value(key).split(':', 1)

    if len(values) < 1:

        raise ValueError('Invalid time value "{0}", expected "{1}"!'
                         .format(value(key), 'HH:MM or just HH'))

    hour   = __int__(values[0])
    minute = __int__(values[1]) \
             if len(values) > 1 \
             else 0

    return datetime.time(hour, minute)

def list(key, default=None, format='{0}'):

    if not has(key): return default

    return [ format.format(_.strip()) for _ in value(key).split(' ') if _.strip() ]

def enum(enum, key, default=None):

    if not has(key): return default

    for item in enum:

        if not item.name == value(key):
            continue

        return item

    raise ValueError('No matching item "{0}" found in enum "{1}"!'
                     .format(value(key), str(enum)))
