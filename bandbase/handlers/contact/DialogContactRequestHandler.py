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

class DialogContactRequestHandler(RequestHandler):

    def add_get(self):

        with database.session() as db:

            contact = Contact()

            categories = db.query(ContactCategory) \
                           .order_by(ContactCategory.Name) \
                           .all()

            return response.template('contact_form.html', \
                                     contact=contact, \
                                     categories=categories)

    def add_post(self):

        with database.session() as db:

            contact = Contact()

            try:

                parser = ContactFormRequestParser(db=db)

                parser.parse(contact)

                db.add(contact)
                db.commit()

                data = \
                {
                    'id':   int(contact),
                    'name': str(contact)
                }

                return response.json(data)

            except Exception as e:

                db.rollback()

                logger.exception(e)

                data = \
                {
                    'error': str(e)
                }

                return response.json(data)
