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

from datetime import datetime, timedelta

class JsonGigCalendarRequestHandler(RequestHandler):

    def __init__(self, include_private_gigs, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.include_private_gigs = include_private_gigs
        self.today = datetime.today().date()
        self.yesterday = self.today - timedelta(days=1)

    def handle_get(self):

        events = []

        with database.session() as db:

            gigs = db.query(Gig).join(Contact, Gig.Location)

            gigs = gigs.filter(Gig.BeginDate >= self.yesterday)
            gigs = gigs.filter(Gig.IsPublished)

            if not self.include_private_gigs:
                gigs = gigs.filter(Gig.IsPublic)

            gigs = gigs.order_by(sql.ASC(Gig.BeginDate)).all()

            for gig in gigs:

                event = \
                {
                    'id':   gig.ID,
                    'name': gig.Name,
                    'location':
                    {
                        'name':    gig.Location.Name,
                        'address': gig.Location.Address,
                        'latlng':  (gig.Location.Latitude, gig.Location.Longitude)
                                   if gig.Location.Latitude and gig.Location.Longitude
                                   else None
                    },
                    'date':    filters.date(gig.BeginDate),
                    'weekday': filters.weekday(gig.BeginDate),
                    'time':    filters.time(gig.BeginTime),
                }

                events.append(event)

        callback = request.str('callback')

        return response.json(events, callback=callback)
