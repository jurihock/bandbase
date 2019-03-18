from app import app

import utils.logger as logger
import utils.flash as flash
import utils.request as request
import utils.response as response

from handlers.score import *

@app.route('/scores/', methods=['GET'])
@app.https
@app.login
def score_query():

    format = request.str('format')

    if format == 'json':

        handler = JsonScoreRequestHandler()

    else:

        handler = DefaultScoreRequestHandler()

    return handler.query()

@app.route('/score/add', methods=['GET', 'POST'])
@app.https
@app.login
def score_add():

    handler = DefaultScoreRequestHandler()

    return handler.add()

@app.route('/score/<int:id>', methods=['GET', 'POST'])
@app.https
@app.login
def score_update(id):

    handler = DefaultScoreRequestHandler(id=id)

    return handler.update()

@app.route('/score/delete/<int:id>', methods=['GET', 'POST'])
@app.https
@app.login
def score_delete(id):

    handler = DefaultScoreRequestHandler(id=id)

    return handler.delete()

@app.route('/scores.tex', methods=['GET'])
@app.https
@app.login
def score_download_tex():

    import utils.response as response
    import utils.database as database
    from utils.models import Score

    with database.session() as db:

        scores = db.query(Score).order_by(Score.Name).all()

        tex = response.template('score_download.tex', \
                                scores=scores)

        return response.tex(tex, 'Notenkatalog.tex')

@app.route('/scores.pdf', methods=['GET'])
@app.https
@app.login
def score_download_pdf():

    import utils.response as response
    import utils.database as database
    import utils.latex as latex
    from utils.models import Score

    with database.session() as db:

        scores = db.query(Score).order_by(Score.Name).all()

        tex = response.template('score_download.tex', \
                                scores=scores)

        pdf = latex.compile('scores.tex', tex)[1]

        return response.pdf(pdf, 'Notenkatalog.pdf')

@app.route('/score/folders/', methods=['GET'])
@app.route('/score/folder/<int:id>', methods=['GET'])
@app.https
@app.login
def score_folder_query(id=None):

    handler = DefaultScoreFolderItemRequestHandler(id=id)

    return handler.query()

@app.route('/score/folder/<int:id>/add', methods=['POST'])
@app.https
@app.login
def score_folder_item_add(id):

    handler = DefaultScoreFolderItemRequestHandler(id=id)

    return handler.add()

@app.route('/score/folder/<int:id>/delete/<order>', methods=['GET'])
@app.https
@app.login
def score_folder_item_delete(id, order):

    handler = DefaultScoreFolderItemRequestHandler(id=id, order=order)

    return handler.delete()

@app.route('/score/folders.tex', methods=['GET'])
@app.route('/score/folder/<int:id>.tex', methods=['GET'])
@app.https
@app.login
def score_folder_download_tex(id=None):

    handler = TexScoreFolderDownloadRequestHandler(id=id)

    return handler.query()

@app.route('/score/folders.pdf', methods=['GET'])
@app.route('/score/folder/<int:id>.pdf', methods=['GET'])
@app.https
@app.login
def score_folder_download_pdf(id=None):

    handler = PdfScoreFolderDownloadRequestHandler(id=id)

    return handler.query()
