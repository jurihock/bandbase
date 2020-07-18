from app import app

import utils.logger as logger
import utils.flash as flash
import utils.request as request
import utils.response as response

from handlers.contact import *

@app.route('/contacts/', methods=['GET'])
@app.https
@app.login
def contact_query():

    format = request.str('format')

    if format == 'json':

        handler = JsonContactRequestHandler()

    else:

        handler = DefaultContactRequestHandler()

    return handler.query()

@app.route('/contact/add', methods=['GET', 'POST'])
@app.https
@app.login
def contact_add():

    format = request.str('format')

    if format == 'dialog':

        handler = DialogContactRequestHandler()

    else:

        handler = DefaultContactRequestHandler()

    return handler.add()

@app.route('/contact/<int:id>', methods=['GET', 'POST'])
@app.https
@app.login
def contact_update(id):

    handler = DefaultContactRequestHandler(id=id)

    return handler.update()

@app.route('/contact/delete/<int:id>', methods=['GET', 'POST'])
@app.https
@app.login
def contact_delete(id):

    handler = DefaultContactRequestHandler(id=id)

    return handler.delete()

@app.route('/contact/<int:id>.vcf', methods=['GET'])
@app.https
@app.login
def contact_download_vcard(id):

    handler = VcfContactDownloadRequestHandler(id=id)

    return handler.handle()

@app.route('/musicians.pdf', methods=['GET'])
@app.https
@app.login
def contact_musicians_download_pdf():

    handler = PdfMusiciansDownloadRequestHandler()

    return handler.handle()

@app.route('/musicians.tex', methods=['GET'])
@app.https
@app.login
def contact_musicians_download_tex():

    handler = TexMusiciansDownloadRequestHandler()

    return handler.handle()

@app.route('/musicians.csv', methods=['GET'])
@app.https
@app.login
def contact_musicians_download_csv():

    handler = CsvMusiciansDownloadRequestHandler()

    return handler.handle()

@app.route('/birthdays.ics', methods=['GET'])
def contact_musicians_download_ics():

    handler = IcsMusiciansDownloadRequestHandler()

    return handler.handle()
