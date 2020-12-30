from parsers.common import *
from utils.models import *

class ScorePersonsFormRequestParser(RequestParser):

    def parse(self, score):

        def has(score_person_list, score_person):

            if score_person_list is None:
                return False

            person_id = int(score_person.PersonID)
            role_id = int(score_person.PersonRoleID)

            person_ids = [ int(person.PersonID) \
                           for person in score_person_list \
                           if person.PersonRoleID == role_id ]

            return person_id in person_ids

        field_indices = range(0, 5)

        composers = [ self.int('composer' + str(i)) for i in field_indices ]
        arrangers = [ self.int('arranger' + str(i)) for i in field_indices ]
        poets     = [ self.int('poet' + str(i)) for i in field_indices ]

        composers = [ ScorePerson(ScoreID=score.ID, PersonID=composer, PersonRoleID=1)
                      for composer in composers
                      if composer is not None]
        arrangers = [ ScorePerson(ScoreID=score.ID, PersonID=arranger, PersonRoleID=2)
                      for arranger in arrangers
                      if arranger is not None]
        poets     = [ ScorePerson(ScoreID=score.ID, PersonID=poet, PersonRoleID=3)
                      for poet in poets
                      if poet is not None]

        oldPersons = list(score.Persons)
        newPersons = composers + arrangers + poets

        for person in oldPersons:

            if has(newPersons, person):
                continue

            score.Persons.remove(person)

        for person in newPersons:

            if has(oldPersons, person):
                continue

            score.Persons.append(person)
