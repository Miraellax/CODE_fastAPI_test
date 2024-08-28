import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import User, Note

dotenv.load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_NAME")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URL)
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
    User(id=3, username="third", password="333"),
]
notes = [
    Note(owner_id=2, content="test note text"),
    Note(owner_id=3, content="one more"),
    Note(owner_id=3, content="another good note"),
]


def init_data():
    with session_maker() as session:
        try:
            for user in users:
                session.add(user)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e

    with session_maker() as session:
        try:
            for note in notes:
                session.add(note)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
