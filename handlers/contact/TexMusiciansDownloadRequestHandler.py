from app import app

from handlers.common import *
from parsers.contact import *
from utils.models import *

import utils.logger as logger
import utils.flash as flash
import utils.filters as filters
import utils.request as request
import utils.response as response
import utils.database as database

class TexMusiciansDownloadRequestHandler(RequestHandler):

    def handle_get(self):

        with database.session() as db:

            persons = db.query(Contact) \
                        .filter(Contact.IsBandMusician) \
                        .order_by(Contact.LastName) \
                        .all()

            tex = response.template('contact_musicians_download.tex', \
                                    persons=persons)

            return response.tex(tex, 'Musikerliste.tex')
