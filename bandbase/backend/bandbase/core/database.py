import contextlib
import functools
import sqlalchemy
import sqlalchemy.orm


@functools.lru_cache()
def get_session_factory():

    # url = 'postgresql://postgres@localhost:5432/bandbase'
    url = 'postgresql://localhost:5432/bandbase'

    engine = sqlalchemy.create_engine(url)
    sessionmaker = sqlalchemy.orm.sessionmaker()
    sessionmaker.configure(bind=engine)

    return sessionmaker


@contextlib.contextmanager
def session(autocommit=False):

    factory = get_session_factory()
    session = factory()

    try:
        yield session
        if autocommit: session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
