if __name__ == '__main__':

    from app import app

    import utils.database as database

    from utils.models import *

    database.setup(app)

    with database.session(commit=True) as db:

        engine = db.get_bind()

        TableBase.metadata.create_all(engine)

    with database.session(commit=True) as db:

        sequences = \
        [
            'Gigs',
            'Contacts',
            'ContactCategories',
            'Scores',
            'ScoreFolders',
        ]

        for sequence in sequences:

            db.execute('SELECT setval(\'"{0}_ID_seq"\', {1});'.format(sequence, 999))

        objects = \
        [
            # https://www.iban.com/currency-codes
            Currency(ID=276, Name='DEM'),
            Currency(ID=978, Name='EUR'),
            Currency(ID=840, Name='USD')
        ]

        for object in objects:

            db.add(object) if not object.ID else db.merge(object)
