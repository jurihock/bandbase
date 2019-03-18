if __name__ == '__main__':

    from app import app

    import click
    import os
    import urllib.parse

    app.setup()

    click.secho(' * Registering filters {0}'.format(os.path.join(app.directory, 'filters')))
    from utils.filters import *

    click.secho(' * Registering views {0}'.format(os.path.join(app.directory, 'views')))
    from views import *

    url  = app.config['FLASK']
    host = urllib.parse.urlparse(url).hostname
    port = urllib.parse.urlparse(url).port

    debug = app.config['DEBUG']

    app.logger.info('Running on {0}'.format(url))

    if 'PEM' in app.config:

        pem = app.config['PEM']

        publickey  = os.path.join(pem, 'public.pem')
        privatekey = os.path.join(pem, 'private.pem')

        keys = (publickey, privatekey)

        app.run(host=host, port=port, debug=debug, ssl_context=keys)

    else:

        app.run(host=host, port=port, debug=debug)
