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

import flask

class JsonGigRequestHandler(RequestHandler):

    def query_get(self):

        def format_gig_visibility(id):

            def wrap(content):

                return '<div style="display:block;text-align:center;font-family:monospace">' + content + '</div>'

            if   id == 0: return wrap('<span class="label" style="background:#777" title="Versteckt">&nbsp;&nbsp;&nbsp;</span>')
            elif id == 1: return wrap('<span class="label" style="background:#070" title="Kalender">KAL</span>')
            elif id == 2: return wrap('<span class="label" style="background:#007" title="Webseite">WEB</span>')
            elif id == 3: return wrap('<span class="label" style="background:#700" title="Flyer">FLY</span>')

        with database.session() as db:

            parser = GigQueryRequestParser(db=db)

            (gigs, total) = parser.parse()

            data = \
            {
                'total_rows':
                    total,

                'rows':
                [
                    [
                        gig.Name,
                        filters.datetuple(*gig.DateTuple),
                        gig.Location.Name,
                        gig.Comment or '',
                        format_gig_visibility(gig.VisibilityID),
                        [
                            ('update', flask.url_for('gig_update', id=int(gig))),
                            ('delete', flask.url_for('gig_delete', id=int(gig))),
                        ]
                    ]
                    for gig in gigs
                ]
            }

            return response.json(data)
