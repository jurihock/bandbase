from app import app

import utils.logger as logger
import utils.flash as flash
import utils.request as request
import utils.response as response
import utils.database as database
import utils.sql as sql

from utils.models import *

@app.route('/search/gema/', methods=['GET'])
@app.route('/search/gema/<term>', methods=['GET'])
@app.https
@app.login
def search_gema(term=''):

    return response.template('search_gema.html', term=term)

@app.route('/search/contact/', methods=['POST'])
@app.https
@app.login
def search_contact():

    term = request.str('term', format='%{0}%')

    with database.session() as db:

        query = db.query(Contact)

        # FIXME: however, the filter seems to be broken now...
        # .filter(not Contact.IsScorePublisher)
        # .filter(not Contact.IsScorePerson)

        if term: query = query.filter(Contact.FirstName.ilike(term) |
                                      Contact.LastName.ilike(term) |
                                      Contact.FullLastName.ilike(term))

        query = query.order_by(sql.IGNORECASE(Contact.LastName))

        # print(query)

        contacts = query.all()

        data = \
        [
            { 'label': str(contact), 'value': int(contact) }
                for contact in contacts
        ]

        return response.json(data)

@app.route('/search/score/', methods=['POST'])
@app.https
@app.login
def search_score():

    term = request.str('term', format='%{0}%')

    with database.session() as db:

        query = db.query(Score)

        if term: query = query.filter(Score.Name.ilike(term) |
                                      Score.Opus.ilike(term) |
                                      Score.Piece.ilike(term) |
                                      sql.CAST(Score.StockNumber, String(5)).ilike(term))

        query = query.order_by(sql.IGNORECASE(Score.Name))

        scores = query.all()

        data = \
        [
            { 'label': str(score), 'value': int(score) }
                for score in scores
        ]

        return response.json(data)

@app.route('/search/score/person/', methods=['POST'])
@app.https
@app.login
def search_score_person():

    term = request.str('term', format='%{0}%')

    with database.session() as db:

        query = db.query(Contact).filter(Contact.IsScorePerson)

        if term: query = query.filter(Contact.FirstName.ilike(term) |
                                      Contact.LastName.ilike(term) |
                                      Contact.FullLastName.ilike(term))

        query = query.order_by(sql.IGNORECASE(Contact.LastName))

        persons = query.all()

        data = \
        [
            { 'label': str(person), 'value': int(person) }
                for person in persons
        ]

        return response.json(data)

@app.route('/search/gig/person/', methods=['POST'])
@app.https
@app.login
def search_gig_person():

    term = request.str('term', format='%{0}%')

    with database.session() as db:

        query = db.query(Contact).filter(Contact.IsGigPerson)

        if term: query = query.filter(Contact.FirstName.ilike(term) |
                                      Contact.LastName.ilike(term) |
                                      Contact.FullLastName.ilike(term))

        query = query.order_by(
            sql.IGNORECASE(Contact.LastName),
            sql.IGNORECASE(Contact.FirstName))

        persons = query.all()

        data = \
        [
            { 'label': str(person), 'value': int(person) }
                for person in persons
        ]

        return response.json(data)

@app.route('/search/gig/persons/default', methods=['POST'])
@app.https
@app.login
def search_gig_persons_default():

    with database.session() as db:

        persons = db.query(Contact) \
            .filter(Contact.IsBandMusician) \
            .order_by(sql.IGNORECASE(Contact.LastName)) \
            .order_by(sql.IGNORECASE(Contact.FirstName)) \
            .all()

        persons = sorted(persons, key=lambda person: [person.LastName])

        persons = [GigPerson(Person=person,
                             PersonID=person.ID,
                             InstrumentID=0,
                             AttendanceID=1,
                             Comment=None)
                   for person in persons]

        data = \
        [
            {
                'id': int(person.Person),
                'name': str(person.Person),
                'instrument': person.InstrumentID,
                'attendance': person.AttendanceID,
                'comment': person.Comment,
            }
            for person in persons
        ]

        return response.json(data)

@app.route('/search/gig/persons/last', methods=['POST'])
@app.https
@app.login
def search_gig_persons_last():

    with database.session() as db:

        other_gig = db.query(Gig).filter(Gig.Persons.any())

        if request.has('gig'):

            other_gig = other_gig.filter(Gig.ID != request.int('gig'))

        if request.has('date'):

            other_gig = other_gig.filter(Gig.BeginDate < request.date('date'))

        other_gig = other_gig.order_by(sql.DESC(Gig.BeginDate)).first()

        if other_gig is None:

            return response.json([])

        persons = sorted(other_gig.Persons, key=lambda person: [person.Instrument.Name, person.Person.LastName])

        persons = [GigPerson(Person=person.Person,
                             PersonID=person.PersonID,
                             InstrumentID=person.InstrumentID,
                             AttendanceID=1,
                             Comment=None)
                   for person in persons
                   if person.Person.IsBandMusician]

        data = \
        [
            {
                'id': int(person.Person),
                'name': str(person.Person),
                'instrument': person.InstrumentID,
                'attendance': person.AttendanceID,
                'comment': person.Comment,
            }
            for person in persons
        ]

        return response.json(data)

@app.route('/search/gig/scores/last', methods=['POST'])
@app.https
@app.login
def search_gig_scores_last():

    with database.session() as db:

        other_gig = db.query(Gig).filter(Gig.Scores.any())

        if request.has('gig'):

            other_gig = other_gig.filter(Gig.ID != request.int('gig'))

        if request.has('date'):

            other_gig = other_gig.filter(Gig.BeginDate < request.date('date'))

        other_gig = other_gig.order_by(sql.DESC(Gig.BeginDate)).first()

        if other_gig is None:

            return response.json([])

        scores = list(other_gig.Scores)

        data = \
        [
            {
                'id': int(score.Score),
                'name': str(score.Score),
                'order': score.ScoreOrder
            }
            for score in scores
        ]

        return response.json(data)

@app.route('/search/score/publisher/', methods=['POST'])
@app.https
@app.login
def search_score_publisher():

    term = request.str('term', format='%{0}%')

    with database.session() as db:

        query = db.query(Contact).filter(Contact.IsScorePublisher)

        if term: query = query.filter(Contact.FirstName.ilike(term) |
                                      Contact.LastName.ilike(term) |
                                      Contact.FullLastName.ilike(term))

        query = query.order_by(sql.IGNORECASE(Contact.LastName))

        publishers = query.all()

        data = \
        [
            { 'label': str(publisher), 'value': int(publisher) }
                for publisher in publishers
        ]

        return response.json(data)
