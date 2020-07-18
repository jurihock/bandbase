from app import app

from handlers.common import *
from parsers.score import *
from utils.models import *

import utils.logger as logger
import utils.flash as flash
import utils.filters as filters
import utils.request as request
import utils.response as response
import utils.database as database

class DefaultScoreRequestHandler(RequestHandler):

    def query_get(self):

        return response.template('score_query.html')

    def add_get(self):

        with database.session() as db:

            score = Score()

            editions = db.query(ScoreEdition).all()
            gemaTypes = db.query(ScoreGemaType).all()

            return response.template('score_add.html',
                                     score=score,
                                     editions=editions,
                                     gemaTypes=gemaTypes)

    def add_post(self):

        with database.session() as db:

            score = Score()

            editions = db.query(ScoreEdition).all()
            gemaTypes = db.query(ScoreGemaType).all()

            try:

                parsers = \
                [
                    ScoreFormRequestParser(db=db),
                    ScorePersonsFormRequestParser(db=db),
                    ScoreLineupFormRequestParser(db=db)
                ]

                for parser in parsers:
                    parser.parse(score)

                db.add(score)
                db.commit()

                flash.success('Musikstück <a href="{0}">{1}</a> wurde erfolgreich hinzugefügt!'
                              .format(flask.url_for('score_update', id=int(score)), str(score)))

                return response.redirect('score_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('score_add.html',
                                         score=score,
                                         editions=editions,
                                         gemaTypes=gemaTypes)

    def update_get(self):

        with database.session() as db:

            score = db.query(Score).get(self.id)

            editions = db.query(ScoreEdition).all()
            gemaTypes = db.query(ScoreGemaType).all()

            return response.template('score_update.html',
                                     score=score,
                                     editions=editions,
                                     gemaTypes=gemaTypes)

    def update_post(self):

        with database.session() as db:

            score = db.query(Score).get(self.id)

            editions = db.query(ScoreEdition).all()
            gemaTypes = db.query(ScoreGemaType).all()

            try:

                parsers = \
                [
                    ScoreFormRequestParser(db=db),
                    ScorePersonsFormRequestParser(db=db),
                    ScoreLineupFormRequestParser(db=db)
                ]

                for parser in parsers:
                    parser.parse(score)

                db.commit()

                flash.success('Musikstück <a href="{0}">{1}</a> wurde erfolgreich aktualisiert!'
                              .format(flask.url_for('score_update', id=int(score)), str(score)))

                return response.redirect('score_query')

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.template('score_update.html',
                                         score=score,
                                         editions=editions,
                                         gemaTypes=gemaTypes)

    def delete_get(self):

        with database.session() as db:

            score = db.query(Score).get(self.id)

            return response.template('score_delete.html',
                                     score=score)

    def delete_post(self):

        with database.session() as db:

            score = db.query(Score).get(self.id)

            try:

                if score.IsPersistent: raise PersistentEntryError()
                if score.IsRelated:    raise RelatedEntryError()

                logger.info('Deleting score {0}, {1}.'.format(int(score), str(score)))

                db.delete(score)
                db.commit()

                flash.success('Musikstück <em>{0}</em> wurde erfolgreich gelöscht!'.format(str(score)))

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

        return response.redirect('score_query')
