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
import utils.latex as latex

import os
import subprocess

class PdfGigSetlistRequestHandler(RequestHandler):

    def handle_get(self):

        with database.session() as db:

            gig = db.query(Gig).get(self.id)

            query = sql.QUERY(
                '''
                select "Scores"."Name" as "Name", min("GigScores"."ScoreOrder") as "Order", string_agg("ScoreFolderItems"."ScoreOrder", ',') as "Number"
                from "GigScores"
                left join "ScoreFolderItems"
                on "GigScores"."ScoreID" = "ScoreFolderItems"."ScoreID"
                left join "Scores"
                on "GigScores"."ScoreID" = "Scores"."ID"
                where "GigScores"."GigID" = {0}
                group by "GigScores"."ScoreID", "Scores"."Name"
                order by min("GigScores"."ScoreOrder");
                '''.format(int(gig)))

            scores = db.execute(query).fetchall()

            tex = response.template('gig_setlist_download.tex',
                                    gig=gig,
                                    scores=scores)

            setlist_filename = 'Setlist {0} {1}.pdf'.format(
                str(gig), filter.datetuple(*gig.DateTuple))

        the_filename  = 'setlist'
        tex_filename  = the_filename + '.tex'
        pdf1_filename = the_filename + '.pdf'
        pdf2_filename = the_filename + '_clone.pdf'
        pdf3_filename = the_filename + '_print.pdf'
        pdf4_filename = the_filename + '_final.pdf'

        latex.compile(tex_filename, tex, read=False)
        latex.clone(pdf1_filename, pdf2_filename, read=False)
        latex.jam(pdf2_filename, pdf3_filename, read=False)
        pdf = latex.merge([pdf1_filename, pdf3_filename], pdf4_filename)[1]

        return response.pdf(setlist_filename, pdf)