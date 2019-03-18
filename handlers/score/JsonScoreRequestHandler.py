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

class JsonScoreRequestHandler(RequestHandler):

    def query_get(self):

        with database.session() as db:

            parser = ScoreQueryRequestParser(db=db)

            (scores, total) = parser.parse()

            data = \
            {
                'total_rows':
                    total,

                'rows':
                [
                    [
                        score.NameOpusPiece,
                        score.StockLetter or '',
                        score.StockNumberCounter or '',
                        score.Edition.Name or '',
                        score.GSM or '',
                        score.Comment or '',
                        [
                            ('update', flask.url_for('score_update', id=int(score))),
                            ('delete', flask.url_for('score_delete', id=int(score)))
                            if not score.IsPersistent else '',
                        ]
                    ]
                    for score in scores
                ]
            }

            return response.json(data)
