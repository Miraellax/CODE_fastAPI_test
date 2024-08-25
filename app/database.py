from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import Note, User

DB_USER = "postgres"
DB_PASSWORD = "123963"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "CODE_fastapi_db"

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


users = [
    User(id=1, username="first", password="111"),
    User(id=2, username="second", password="222"),
    User(id=3, username="third", password="333")
]
notes = [
    Note(id=1, owner_id=2, content="test note text"),
    Note(id=2, owner_id=3, content="one more"),
    Note(id=3, owner_id=3, content="another good note")
]


def init_data():
    with session_maker() as session:
        try:
            for user in users:
                session.add(user)
        except Exception as e:
            session.rollback()
            raise e
        else:
            session.commit()

    with session_maker() as session:
        try:
            for note in notes:
                session.add(note)
        except Exception as e:
            session.rollback()
            raise e
        else:
            session.commit()


