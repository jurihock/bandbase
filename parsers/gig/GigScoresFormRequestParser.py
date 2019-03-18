from parsers.common import *
from utils.models import *

class GigScoresFormRequestParser(RequestParser):

    def parse(self, gig):

        field_count = self.int('gig_scores_field_count')
        field_indices = range(field_count)

        scores = [ self.int('score' + str(i))
                   for i in field_indices ]

        scores = [ GigScore(GigID=gig.ID, ScoreID=score_id, ScoreOrder=score_order)
                   for (score_order, score_id) in enumerate(scores)
                   if score_id is not None]

        gig.Scores.clear()

        for score in scores:

            gig.Scores.append(score)
