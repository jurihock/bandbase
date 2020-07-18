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
import utils.sql as sql

import flask

from datetime import datetime

class DefaultGigRequestHandler(RequestHandler):

    def query_get(self):

        count = 10

        with database.session() as db:

            count = max(count, db.query(Gig).filter(sql.EXTRACT('year', Gig.BeginDate) >= datetime.today().year).count())

        return response.template('gig_query.html', count=count)

    def add_get(self):

        with database.session() as db:

            gig = Gig()

            gig.build(db)

            gemaTypes = db.query(GigGemaType).all()
            visibilities = db.query(GigVisibility).all()
            instruments = db.query(MusicalInstrument).order_by(MusicalInstrument.Name).all()
            attendances = db.query(GigPersonAttendance).order_by(GigPersonAttendance.Name).all()

            return response.template('gig_add.html',
                                     gig=gig,
                                     gemaTypes=gemaTypes,
                                     visibilities=visibilities,
                                     instruments=instruments,
                                     attendances=attendances)

    def add_post(self):

        with database.session() as db:

            gig = Gig()

            gig.build(db)

            gemaTypes = db.query(GigGemaType).all()
            visibilities = db.query(GigVisibility).all()
            instruments = db.query(MusicalInstrument).order_by(MusicalInstrument.Name).all()
            attendances = db.query(GigPersonAttendance).order_by(GigPersonAttendance.Name).all()

            try:

                parsers = \
                [
                    GigFormRequestParser(db=db),
                    GigScoresFormRequestParser(db=db),
                    GigPersonsFormRequestParser(db=db),
                    GigGemaFormRequestParser(db=db)
                ]

                for parser in parsers:
                    parser.parse(gig)

                db.add(gig)
                db.commit()

                flash.success('Gig <a href="{0}">{1}</a> wurde erfolgreich hinzugefügt!'
                              .format(flask.url_for('gig_update', id=int(gig)), str(gig)))

                return response.redirect('gig_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('gig_add.html', \
                                         gig=gig,
                                         gemaTypes=gemaTypes,
                                         visibilities=visibilities,
                                         instruments=instruments,
                                         attendances=attendances)

    def update_get(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            gig.build(db)

            gemaTypes = db.query(GigGemaType).all()
            visibilities = db.query(GigVisibility).all()
            instruments = db.query(MusicalInstrument).order_by(MusicalInstrument.Name).all()
            attendances = db.query(GigPersonAttendance).order_by(GigPersonAttendance.Name).all()

            return response.template('gig_update.html', \
                                     gig=gig,
                                     gemaTypes=gemaTypes,
                                     visibilities=visibilities,
                                     instruments=instruments,
                                     attendances=attendances)

    def update_post(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            gig.build(db)

            gemaTypes = db.query(GigGemaType).all()
            visibilities = db.query(GigVisibility).all()
            instruments = db.query(MusicalInstrument).order_by(MusicalInstrument.Name).all()
            attendances = db.query(GigPersonAttendance).order_by(GigPersonAttendance.Name).all()

            try:

                parsers = \
                [
                    GigFormRequestParser(db=db),
                    GigScoresFormRequestParser(db=db),
                    GigPersonsFormRequestParser(db=db),
                    GigGemaFormRequestParser(db=db)
                ]

                for parser in parsers:
                    parser.parse(gig)

                db.commit()

                flash.success('Gig <a href="{0}">{1}</a> wurde erfolgreich aktualisiert!'
                              .format(flask.url_for('gig_update', id=int(gig)), str(gig)))

                return response.redirect('gig_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('gig_update.html', \
                                         gig=gig,
                                         gemaTypes=gemaTypes,
                                         visibilities=visibilities,
                                         instruments=instruments,
                                         attendances=attendances)

    def delete_get(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            return response.template('gig_delete.html',
                                     gig=gig)

    def delete_post(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            try:

                if gig.IsPersistent: raise PersistentEntryError()
                if gig.IsRelated:    raise RelatedEntryError()

                logger.info('Deleting gig {0}, {1}.'.format(int(gig), str(gig)))

                db.delete(gig)
                db.commit()

                flash.success('Gig <em>{0}</em> wurde erfolgreich gelöscht!'
                              .format(str(gig)))

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

            return response.redirect('gig_query')
