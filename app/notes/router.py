from typing import Annotated, Union

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.notes import dao as notes_dao
from app.users import dao as users_dao
from app.notes import schema as notes_schema
from app.models.models import Note

router = APIRouter(prefix="/notes")


@router.post("/post/{owner_id}", response_model=notes_schema.Note)
def post_note(
    note: notes_schema.NoteCreate,
    credentials: Annotated[HTTPBasicCredentials, Depends(users_dao.check_auth)],
    db: Session = Depends(get_db),
) -> Union[Note, None]:
    if credentials is not None:
        # При отсутствии доступа check_auth выдаст исключение
        db_note = notes_dao.create_note(db, note=note)
        return db_note


@router.post("/post/current", response_model=notes_schema.Note)
def post_note_current(
    note_content: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(users_dao.check_auth)],
    db: Session = Depends(get_db),
) -> Union[Note, None]:
    if credentials is not None:
        # При отсутствии доступа check_auth выдаст исключение
        db_user_id = users_dao.get_user_id(db, credentials)

        if db_user_id is not None:
            db_note = notes_dao.create_note(
                db,
                note=notes_schema.NoteCreate(owner_id=db_user_id, content=note_content),
            )
            return db_note
