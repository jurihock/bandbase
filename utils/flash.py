import flask

def info(message):

    flask.flash(message, category='info')

def success(message):

    flask.flash(message, category='success')

def warning(message):

    flask.flash(message, category='warning')

def error(message):

    flask.flash(message, category='danger')
