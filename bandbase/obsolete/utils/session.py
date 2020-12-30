import flask

def has(key):

    return key in flask.session

def get(key, default=None):

    return flask.session[key] if has(key) else default

def set(key, value):

    flask.session[key] = value

def clear(key):

    flask.session.pop(key, None)
