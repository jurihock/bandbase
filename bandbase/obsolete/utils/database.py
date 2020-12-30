import click
import sqlalchemy
import sqlalchemy.orm
import contextlib

__session__ = sqlalchemy.orm.sessionmaker()

def setup(app):

    url = app.config['DATABASE']

    click.secho(' * Setting up database {0}'.format(url))

    engine = sqlalchemy.create_engine(url)

    __session__.configure(bind=engine)

@contextlib.contextmanager
def session(commit=False):

    session = __session__()

    try:
        yield session
        if commit: session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
