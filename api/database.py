from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.env_var import SQLITE_PATH
from api.models import Base


class Database:
    _session = None

    def __init__(self):
        self.get_session()

    def get_session(self):
        if self._session is None:
            self._create_session()
        return self._session

    def delete_session(self):
        self._session.close_all()
        del self._session

    def _create_session(self):
        engine = create_engine(f"sqlite:///{SQLITE_PATH}")
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self._session = Session()
