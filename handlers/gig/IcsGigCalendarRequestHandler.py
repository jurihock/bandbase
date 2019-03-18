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

from icalendar import Calendar, Event
from datetime import datetime
from pytz import timezone

class IcsGigCalendarRequestHandler(RequestHandler):

    def __init__(self, include_private_gigs, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.include_private_gigs = include_private_gigs
        self.today = datetime.today().date()

    def handle_get(self):

        calendar = Calendar()

        #calendar.add('method', 'PUBLISH')
        #calendar.add('calscale', 'GREGORIAN')

        if self.include_private_gigs:

            calendar.add('x-wr-calname', 'Big Band - Gigs')
            calendar.add('x-wr-caldesc', 'Privater Terminkalender der Big Band „Brandheiß“ Pforzheim')

        else:

            calendar.add('x-wr-calname', 'Big Band „Brandheiß“ Pforzheim')
            calendar.add('x-wr-caldesc', 'Öffentlicher Terminkalender der Big Band „Brandheiß“ Pforzheim')

        calendar.add('x-wr-timezone', 'Europe/Berlin')

        tz = timezone('Europe/Berlin')

        with database.session() as db:

            gigs = db.query(Gig).join(Contact, Gig.Location)

            gigs = gigs.filter(Gig.IsPublished)

            if not self.include_private_gigs:
                gigs = gigs.filter(Gig.IsPublic)

            gigs = gigs.order_by(sql.DESC(Gig.BeginDate)).all()

            for gig in gigs:

                event = Event()

                event.add('uid', str(gig.ID))

                if self.include_private_gigs:
                    event.add('summary', 'BB - Gig - {0}'.format(gig.Name))
                else:
                    event.add('summary', gig.Name)

                event.add('location', gig.Location.Name +
                    ' ({0})'.format(gig.Location.Address)
                        if gig.Location.Address else '')

                if gig.Location.Latitude and gig.Location.Longitude:
                    event.add('geo', (gig.Location.Latitude, gig.Location.Longitude))

                event.add('dtstart', datetime(
                    gig.BeginDate.year,
                    gig.BeginDate.month,
                    gig.BeginDate.day,
                    gig.BeginTime.hour,
                    gig.BeginTime.minute,
                    tzinfo=tz))

                event.add('dtend', datetime(
                    gig.EndDate.year,
                    gig.EndDate.month,
                    gig.EndDate.day,
                    gig.EndTime.hour,
                    gig.EndTime.minute,
                    tzinfo=tz))

                event.add('dtstamp', datetime(
                    self.today.year,
                    self.today.month,
                    self.today.day,
                    tzinfo=tz))

                calendar.add_component(event)

        filename = 'BigBandBrandheissPforzheim.ics'
        data = calendar.to_ical()

        return response.ics(data, filename)
