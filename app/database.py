from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager

DATABASE_URL = "sqlite:///association.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


@contextmanager
def db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()