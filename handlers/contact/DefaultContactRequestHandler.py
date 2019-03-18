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
import utils.sql as sql

import flask

class DefaultContactRequestHandler(RequestHandler):

    def query_get(self):

        with database.session() as db:

            musicians = db.query(Contact) \
                .filter(Contact.IsBandMusician) \
                .filter(Contact.EMail.isnot(None)) \
                .order_by(sql.IGNORECASE(Contact.LastName)) \
                .order_by(sql.IGNORECASE(Contact.FirstName)) \
                .all()

            musicians_email_string = '; '.join([ '{0} <{1}>'.format(musician.Name, musician.EMail)
                                                 for musician in musicians ])

        return response.template('contact_query.html',
                                 musicians_email_string=musicians_email_string)

    def add_get(self):

        with database.session() as db:

            contact = Contact()

            categories = db.query(ContactCategory) \
                           .order_by(ContactCategory.Name) \
                           .all()

            return response.template('contact_add.html', \
                                     contact=contact, \
                                     categories=categories)

    def add_post(self):

        with database.session() as db:

            contact = Contact()

            categories = db.query(ContactCategory) \
                           .order_by(ContactCategory.Name) \
                           .all()

            try:

                parser = ContactFormRequestParser(db=db)

                parser.parse(contact)

                db.add(contact)
                db.commit()

                flash.success('Kontakt <a href="{0}">{1}</a> wurde erfolgreich hinzugefügt!'
                              .format(flask.url_for('contact_update', id=int(contact)), str(contact)))

                return response.redirect('contact_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('contact_add.html', \
                                         contact=contact, \
                                         categories=categories)

    def update_get(self):

        with database.session() as db:

            contact = db.query(Contact).get(self.id)

            categories = db.query(ContactCategory) \
                           .order_by(ContactCategory.Name) \
                           .all()

            return response.template('contact_update.html', \
                                     contact=contact, \
                                     categories=categories)

    def update_post(self):

        with database.session() as db:

            contact = db.query(Contact).get(self.id)

            categories = db.query(ContactCategory) \
                           .order_by(ContactCategory.Name) \
                           .all()

            try:

                parser = ContactFormRequestParser(db=db)

                parser.parse(contact)

                db.commit()

                flash.success('Kontakt <a href="{0}">{1}</a> wurde erfolgreich aktualisiert!'
                             .format(flask.url_for('contact_update', id=int(contact)), str(contact)))

                return response.redirect('contact_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('contact_update.html', \
                                         contact=contact, \
                                         categories=categories)

    def delete_get(self):

        with database.session() as db:

            contact = db.query(Contact).get(self.id)

            return response.template('contact_delete.html',
                                     contact=contact)

    def delete_post(self):

        with database.session() as db:

            contact = db.query(Contact).get(self.id)

            try:

                if contact.IsPersistent: raise PersistentEntryError()
                if contact.IsRelated:    raise RelatedEntryError()

                logger.info('Deleting contact {0}, {1}.'.format(int(contact), str(contact)))

                db.delete(contact)
                db.commit()

                flash.success('Kontakt <em>{0}</em> wurde erfolgreich gelöscht!'.format(str(contact)))

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

        return response.redirect('contact_query')
