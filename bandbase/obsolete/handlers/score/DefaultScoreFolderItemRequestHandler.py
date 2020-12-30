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

import flask

class DefaultScoreFolderItemRequestHandler(RequestHandler):

    def __init__(self, order=None, *args, **kwargs):

        super(self).__init__(*args, **kwargs)

        self.order = order

    def query_get(self):

        with database.session() as db:

            folders = db.query(ScoreFolder).order_by(ScoreFolder.Order)

            folders = folders.filter(ScoreFolder.ID == self.id).all() \
                      if self.id is not None \
                      else folders.all()

            return response.template('score_folder_query.html',
                                     folders=folders)

    def add_post(self):

        with database.session() as db:

            folder = db.query(ScoreFolder).get(self.id)

            try:

                parser = ScoreFolderItemFormRequestParser(db=db, folder=folder)

                item = parser.parse()
                db.commit()
                score = item.Score

                flash.success('Musikstück <a href="{0}">{1}</a> wurde erfolgreich zur Notenmappe <em>{2}</em> hinzugefügt!'
                             .format(
                                flask.url_for('score_update', id=int(score)),
                                str(score),
                                str(folder)))

                return response.redirect('score_folder_query', suffix='#{0}'.format(self.id))

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.redirect('score_folder_query')

    def delete_get(self):

        with database.session() as db:

            try:

                folder = db.query(ScoreFolder).get(self.id)

                for item in folder.Items:

                    if item.ScoreOrder != self.order:
                        continue

                    folder.Items.remove(item)
                    db.commit()

                    score = db.query(Score).get(item.ScoreID)

                    flash.success('Musikstück <a href="{0}">{1}</a> wurde erfolgreich aus der Notenmappe <em>{2}</em> entfernt!'
                                  .format(
                                    flask.url_for('score_update', id=int(score)),
                                    str(score),
                                    str(folder)))

                    break

                return response.redirect('score_folder_query', suffix='#{0}'.format(self.id))

            except Exception as e:

                db.rollback()

                logger.exception(e)
                flash.error(str(e))

                return response.redirect('score_folder_query')
