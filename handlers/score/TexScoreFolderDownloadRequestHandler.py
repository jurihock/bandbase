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

class TexScoreFolderDownloadRequestHandler(RequestHandler):

    def query(self):

        with database.session() as db:

            if self.id is not None:

                folder = db.query(ScoreFolder).get(self.id)

                # TODO: what is this? can be removed?
                # items = db.query(ScoreFolderItem).filter(ScoreFolderItem.ScoreFolderID == self.id).all()
                # scores = [item.Score for item in items if len(filter.lines(item.Score.Hyperlinks)) > 0]
                # scores = sorted(scores, key=lambda score: score.Name.lower())

                scores = []  # prevent scores to be printed out, don't need this feature yet

                tex = response.template('score_folder_download.tex', folders=[folder], scores=scores)

                filename = 'Notenmappe {0}.tex'.format(folder.Name)

                return response.tex(tex, filename)

            else:

                folders = db.query(ScoreFolder) \
                            .order_by(ScoreFolder.Order) \
                            .all()

                # TODO: what is this? can be removed?
                # items = db.query(ScoreFolderItem).all()
                # scores = [item.Score for item in items if len(filter.lines(item.Score.Hyperlinks)) > 0]
                # scores = sorted(scores, key=lambda score: score.Name.lower())

                scores = []  # prevent scores to be printed out, don't need this feature yet

                tex = response.template('score_folder_download.tex', folders=folders, scores=scores)

                filename = 'Notenmappen.tex'

                return response.tex(tex, filename)
