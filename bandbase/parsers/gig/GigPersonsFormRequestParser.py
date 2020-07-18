from parsers.common import *
from utils.models import *

class GigPersonsFormRequestParser(RequestParser):

    def parse(self, gig):

        field_count = self.int('gig_persons_field_count')
        field_indices = range(field_count)

        adjust_musician_count = self.bool('adjust_musician_count')

        persons = [ (self.int('person' + str(i)),
                     self.int('instrument' + str(i)),
                     self.int('attendance' + str(i)),
                     self.str('comment' + str(i)))
                    for i in field_indices ]

        persons = [ GigPerson(GigID=gig.ID,
                              PersonID=person_id,
                              InstrumentID=instrument_id,
                              AttendanceID=attendance_id,
                              Comment=comment)
                    for (person_id, instrument_id, attendance_id, comment) in persons
                    if person_id is not None]

        gig.Persons.clear()

        for person in persons:

            gig.Persons.append(person)

        if adjust_musician_count:

            onlyPresentPersons = [ person for person in persons
                                   if person.AttendanceID == 1   # Anwesend
                                   or person.AttendanceID == 3 ] # Aushilfe

            count = len(onlyPresentPersons)

            gig.MusicianCount = count if count > 0 else None
