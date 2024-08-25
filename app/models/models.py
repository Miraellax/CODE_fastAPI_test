from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import declarative_base

# Базовый класс для таблиц базы данных
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
