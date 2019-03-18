from app import app

@app.context_processor
def inject_utcnow():

    from datetime import datetime

    return {'utcnow': datetime.utcnow()}

@app.template_filter('len')
def length(values):

    return len(values)

@app.template_filter('sum')
def sum(values):

    import numpy as np

    return np.sum(values)

@app.template_filter('tex')
def tex(value):

    return value \
        .replace('\\', '\\textbackslash{}') \
        .replace('#', '\\#') \
        .replace('$', '\\$') \
        .replace('%', '\\%') \
        .replace('&', '\\&') \
        .replace('_', '\\_') \
        .replace('{', '\\{') \
        .replace('}', '\\}') \
        .replace('^', '\\^{}') \
        .replace('~', '\\~{}') \
        .replace('"', '"{}') \
        if value is not None \
        else ''

@app.template_filter('url')
def url(value):

    from urllib.parse import unquote

    return unquote(value) \
        if value is not None \
        else ''

@app.template_filter('texurl')
def texurl(value):

    from urllib.parse import unquote

    return unquote(value) \
        .replace('#', '\\#') \
        .replace('&', '\\&') \
        if value is not None \
        else ''

@app.template_filter('str')
def str(value):

    return value \
        if value is not None \
        else ''

@app.template_filter('int')
def int(value):

    from builtins import str as __str__
    from builtins import int as __int__

    return __str__(__int__(value)) \
        if value is not None \
        else ''

@app.template_filter('float')
def float(value):

    from builtins import str as __str__
    from builtins import float as __float__

    return __str__(__float__(value)).replace('.', ',', 1) \
        if value is not None \
        else ''

@app.template_filter('isodate')
def isodate(value):

    import dateutil.parser

    return dateutil.parser.parse(value) \
        if value is not None \
        else None

@app.template_filter('date')
def date(value):

    return value.strftime('%d.%m.%Y') \
        if value is not None \
        else ''

@app.template_filter('day')
def day(value):

    return value.strftime('%d') \
        if value is not None \
        else ''

@app.template_filter('month')
def month(value):

    return value.strftime('%m') \
        if value is not None \
        else ''

@app.template_filter('year')
def year(value):

    return value.strftime('%Y') \
        if value is not None \
        else ''

@app.template_filter('weekday')
def weekday(value):

    if value is None:
        return ''

    weekdays = [ 'MO', 'DI', 'MI', 'DO', 'FR', 'SA', 'SO' ]
    weekday = value.weekday()

    return weekdays[weekday]

@app.template_filter('time')
def time(value):

    return value.strftime('%H:%M') \
        if value is not None \
        else ''

@app.template_filter('datetuple')
def datetuple(begin, end):

    if begin is None and end is None:
        return None

    if begin != end:
        return '{0}-{1}'.format(
            date(begin),
            date(end))

    return date(end)

@app.template_filter('timetuple')
def timetuple(begin, end):

    if begin is None and end is None:
        return None

    if begin != end:
        return '{0}-{1}'.format(
            time(begin),
            time(end))

    return time(end)

@app.template_filter('utcdaydelta')
def utcdaydelta(date, iftoday='heute', ifyesterday='gestern', otherwise='%s Tagen'):

    from datetime import datetime

    left = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    right = date.replace(hour=0, minute=0, second=0, microsecond=0)

    days = (left - right).days

    if days == 0: return iftoday
    elif days == 1: return ifyesterday
    else: return otherwise.format(days)

@app.template_filter('lines')
def lines(value):

    if value is None:
        return []

    lines = [ line for line in value.splitlines() if line ]

    return lines

@app.template_filter('hostname')
def hostname(value):

    from urllib.parse import urlparse

    if value is None:
        return ''

    try:

        url = urlparse(value)

        return url.hostname.replace('www.', '')

    except:

        return value

@app.template_filter('bool')
def bool(value):

    from builtins import bool as __bool__

    return __bool__(value) \
        if value is not None \
        else ''

@app.template_filter('min')
def min(value):

    from builtins import min as __min__

    return __min__(value)

@app.template_filter('max')
def max(value):

    from builtins import max as __max__

    return __max__(value)

@app.template_filter('sorted')
def sorted(items, byattr=None, alphanum=False):

    from builtins import str as __str__
    from builtins import int as __int__
    from builtins import sorted as __sorted__

    def to_alphanum_key(key):

        # http://stackoverflow.com/a/16956262

        from itertools import groupby

        return \
        [
            __int__(''.join(g))
            if k else ''.join(g)
            for k, g in groupby('\0' + key, __str__.isdigit)
        ]

    def get_sort_key(item):

        key = item

        if byattr is not None:

            key = getattr(item, byattr)

        if alphanum:

            key = to_alphanum_key(key)

        return key

    return __sorted__(items, key=lambda item: get_sort_key(item))
