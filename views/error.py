from app import app

import utils.logger as logger
import utils.flash as flash
import utils.request as request
import utils.response as response

@app.errorhandler(404)
@app.login
def E404(error):

    code = 404
    error = 'Die angeforderte Seite will nicht gefunden werden!'

    return response.template('error.html', code=code, error=error), code

@app.errorhandler(401)
@app.login
def E401(error):

    code = 401
    error = 'Unauthorized'

    return response.template('error.html', code=code, error=error), code

@app.errorhandler(500)
@app.login
def E500(error):

    code = 500
    error = 'Internal Server Error'

    return response.template('error.html', code=code, error=error), code
