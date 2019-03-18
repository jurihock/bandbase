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

import flask

class JsonContactRequestHandler(RequestHandler):

    def query_get(self):

        with database.session() as db:

            parser = ContactQueryRequestParser(db=db)

            (contacts, total) = parser.parse()

            data = \
            {
                'total_rows':
                    total,

                'rows':
                [
                    [
                        contact.Name,
                        contact.Category.Name,
                        contact.Comment or '',
                        [
                            ('update', flask.url_for('contact_update', id=int(contact))),
                            ('delete', flask.url_for('contact_delete', id=int(contact)))
                                if not contact.IsPersistent else '',
                        ]
                    ]
                    for contact in contacts
                ]
            }

            return response.json(data)
