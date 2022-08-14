import click
import contextlib
import functools
import sqlalchemy
import sqlalchemy.orm


@functools.lru_cache()
def get_session_maker():

    url = 'postgresql://postgres@localhost:5432/bandbase'

    engine = sqlalchemy.create_engine(url)

    maker = sqlalchemy.orm.sessionmaker()
    maker.configure(bind=engine)

    return maker


@contextlib.contextmanager
def session():

    maker = get_session_maker()
    session = maker()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def bootstrap():

    from bandbase.schemas.database import TableBase, Currency

    sequences = \
    [
        'Gigs',
        'Contacts',
        'ContactCategories',
        'Scores',
        'ScoreFolders',
    ]

    currencies = \
    [
        # https://www.iban.com/currency-codes
        Currency(ID=276, Name='DEM'),
        Currency(ID=978, Name='EUR'),
        Currency(ID=840, Name='USD'),
    ]

    click.secho(f'Init database')

    with session() as db:

        engine = db.get_bind()
        inspector = sqlalchemy.inspect(engine)

        sequences = [ name for name in sequences if not inspector.has_table(name) ]
        currencies = currencies if not inspector.has_table('Currencies') else []

        TableBase.metadata.create_all(engine)

        for sequence in sequences:

            click.secho(f'Init sequence {sequence}')

            db.execute('SELECT setval(\'"{0}_ID_seq"\', {1});'.format(sequence, 999))

        for object in currencies:

            click.secho(f'Init currency {object}')

            db.add(object) if not object.ID else db.merge(object)
