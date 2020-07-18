from app import app

from handlers.common import *
from parsers.gig import *
from utils.models import *

import utils.logger as logger
import utils.flash as flash
import utils.filters as filters
import utils.request as request
import utils.response as response
import utils.database as database

import utils.gema as gema

class GemaMusikfolgeRequestHandler(RequestHandler):

    def handle_get(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            gig.build(db)

            make_flatten_pdf = False  # TODO: Temporary disable readonly pdf generation...

            musikfolge_filepath = gema.make_musikfolge_pdf(gig, make_flatten_pdf)

            with open(musikfolge_filepath, 'rb') as musikfolge_file:

                musikfolge_data = musikfolge_file.read()

            musikfolge_filename = 'GEMA {0} {1}.pdf'.format(
                str(gig), filter.datetuple(*gig.DateTuple))

        return response.pdf(musikfolge_data, musikfolge_filename)
