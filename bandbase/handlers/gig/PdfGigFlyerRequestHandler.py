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
import utils.latex as latex

import os
import shutil

class PdfGigFlyerRequestHandler(RequestHandler):

    def __init__(self, foreground, background, publish=False, *args, **kwargs):

        super(self).__init__(*args, **kwargs)

        self.foreground = foreground
        self.background = background
        self.publish = publish

    def handle_get(self):

        month_to_season = \
        {
            1:  'Winter',
            2:  'Winter',
            3:  'Frühling',
            4:  'Frühling',
            5:  'Frühling',
            6:  'Sommer',
            7:  'Sommer',
            8:  'Sommer',
            9:  'Herbst',
            10: 'Herbst',
            11: 'Herbst',
            12: 'Winter'
        }

        season_index = \
        {
            'Frühling': 1,
            'Sommer':   2,
            'Herbst':   3,
            'Winter':   4
        }

        graphicspath = app.config['FLYER']

        with database.session() as db:

            gigs = db.query(Gig) \
                     .filter(Gig.IsFeatured) \
                     .order_by(Gig.BeginDate) \
                     .all()

            years   = [ str(gig.BeginDate.year) for gig in gigs ]
            months  = [ gig.BeginDate.month for gig in gigs ]
            seasons = [ month_to_season[month] for month in months ]

            # kill duplicates
            seasons = list(set(seasons))
            years   = list(set(years))

            season = '/'.join(sorted(seasons, key=lambda season: season_index[season]))
            year   = '/'.join(sorted(years))

            tex = response.template('gig_flyer_download.tex',
                                    foreground = self.foreground,
                                    background = self.background,
                                    graphicspath=graphicspath,
                                    gigs=gigs,
                                    season=season,
                                    year=year)

        the_filename = 'flyer'
        tex_filename = the_filename + '.tex'
        pdf_filename = the_filename + '.pdf'

        (pdf_path , pdf) = latex.compile(tex_filename, tex)

        if self.publish:

            shutil.copyfile(pdf_path, os.path.join(graphicspath, 'Flyer.pdf'))

            flash.success('Der aktuelle <a href="{0}">Flyer</a> wurde erfolgreich veröffentlicht!'
                          .format('http://bigband-brandheiss.de/flyer.pdf'))

            return response.redirect('gig_query')

        else:

            return response.pdf(pdf, pdf_filename)
