from app import app

from handlers.common import *
from parsers.contact import *
from utils.models import *

import utils.logger as logger
import utils.flash as flash
import utils.filters as filters
import utils.request as request
import utils.response as response
import utils.database as database

from icalendar import Calendar, Event
from pytz import timezone
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta as datedelta

class IcsMusiciansDownloadRequestHandler(RequestHandler):

    def handle_get(self):

        calendar = Calendar()

        #calendar.add('method', 'PUBLISH')
        #calendar.add('calscale', 'GREGORIAN')

        calendar.add('x-wr-calname', 'Big Band - Geburtstage')
        calendar.add('x-wr-caldesc', 'Privater Geburtstagskalender der Big Band „Brandheiß“ Pforzheim')

        calendar.add('x-wr-timezone', 'Europe/Berlin')

        tz = timezone('Europe/Berlin')

        today = datetime.today().date()

        with database.session() as db:

            persons = db.query(Contact) \
                        .filter(Contact.IsBandMusician) \
                        .order_by(Contact.LastName) \
                        .all()

            for person in persons:

                if not person.BirthDate:
                    continue

                for i in [-1, 0, +1]:

                    birthdate = \
                    [
                        person.BirthDate.replace(year=today.year + i),
                        person.BirthDate.replace(year=today.year + i) + timedelta(days=1)
                    ]

                    age = datedelta(birthdate[0], person.BirthDate).years
                    special = ((age % 5) if age > 60 else (age % 10)) == 0

                    event = Event()

                    event.add('uid', str(person.ID) + str(birthdate[0].year))

                    event.add('summary', 'BB - {0} - {1} ({2})'.format(
                        'Runder Geburtstag' if special else 'Geburtstag', person.Name, age))

                    event.add('dtstart', date(
                        birthdate[0].year,
                        birthdate[0].month,
                        birthdate[0].day))

                    event.add('dtend', date(
                        birthdate[1].year,
                        birthdate[1].month,
                        birthdate[1].day))

                    event.add('dtstamp', datetime(
                        today.year,
                        today.month,
                        today.day,
                        tzinfo=tz))

                    calendar.add_component(event)

        data = calendar.to_ical()
        filename = 'BigBandBrandheissPforzheim.ics'

        return response.ics(data, filename)
