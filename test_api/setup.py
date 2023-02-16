from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.models import Base


def setup_database():
    # engine = create_engine(f"sqlite:///{SQLITE_TEST_PATH}")
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def flush_database(session: Session, data_objects: []):
    for do in data_objects:
        session.delete(do)
    session.commit()
    session.flush()
