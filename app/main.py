from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database import engine, init_data
from app.models.models import Base
from app.users.router import router as router_users
from app.notes.router import router as router_notes


init_db = True

if init_db:
    # Создание пустых таблиц в бд, добавление данных для демонстрации
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_data()

app = FastAPI()

app.include_router(router_users)
