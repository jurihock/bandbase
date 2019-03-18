from app import app

import utils.logger as logger
import utils.flash as flash
import utils.request as request
import utils.response as response
import utils.session as session

import numpy as np
from datetime import datetime

@app.route('/')
@app.https
@app.login
def index():

    return response.template('index.html')

@app.route('/bandbase')
@app.https
@app.login
def about():

    return response.template('about.html')

@app.route('/login', methods=['GET', 'POST'])
@app.https
def login():

    if request.ispost():

        session.clear('ok')

        secret = request.str('secret')

        ok = (secret == app.config['LOGIN_SECRET_RO'] and app.config['LOGIN_SECRET_RO']) or \
             (secret == app.config['LOGIN_SECRET_RW'] and app.config['LOGIN_SECRET_RW'])

        if ok:

            session.set('ok', datetime.utcnow().isoformat())

            logger.login(request.ip(), request.agent(), secret, ok)

            if app.config['LOGIN_GREETING']:

                slogans = \
                [
                    'Gut\'s Nächtle!',
                    'Einen wunderschönen guten Morgen!',
                    'Guten Tag!',
                    'Guten Abend!'
                ]

                hour = datetime.now().hour

                timeofday = np.floor((hour + 1) / 6).clip(0, 3).astype(np.int)

                greeting = '<strong>{0}</strong> '.format(slogans[timeofday]) + \
                           'Nun bist du hier bis auf Weiteres angemeldet. ' + \
                           'Solltest du jedoch an einem öffentlich zugänglichen PC arbeiten, ' + \
                           'melde dich bitte nach Benutzung unbedingt wieder ab. ' + \
                           'Denn andernfalls droht die Gefahr, ' + \
                           'dass sich Unbefugte Zugang zu sensiblen Daten verschaffen können! ' + \
                           'Dankend im Voraus, {0}.'.format(app.config['BAND_NAME'].rstrip('.'))

                flash.info(greeting)

            return response.redirect('index')

        logger.login(request.ip(), request.agent(), secret, ok)

        return response.template('login.html', error=True)

    if session.has('ok'):

        return response.redirect('index')

    return response.template('login.html', error=False)

@app.route('/logout')
def logout():

    session.clear('ok')

    logger.logout(request.ip(), request.agent())

    return response.redirect('login')

@app.route('/time')
def time():

    return datetime.now(app.timezone).isoformat()
