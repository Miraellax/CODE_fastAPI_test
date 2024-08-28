from typing import Annotated, Dict, List, Union, Type

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session


from app.database import get_db
from app.notes import schema as notes_schema
from app.users import dao as users_dao
from app.notes import dao as notes_dao
from app.users.dao import check_auth

router = APIRouter(prefix="/users")


@router.get("/current/notes", response_model=List[notes_schema.Note])
def get_current_user_notes(
    credentials: Annotated[HTTPBasicCredentials, Depends(check_auth)],
    db: Session = Depends(get_db),
) -> Union[List[Type[notes_schema.Note]], None]:
    if credentials is not None:
        # В случае отсутствия доступа check_auth выдаст исключение
        owner_id = users_dao.get_user_id(db, credentials)
        if owner_id is not None:
            return notes_dao.get_notes_by_owner(db, owner_id)


@router.post("/current/notes", response_model=notes_schema.Note)
def post_note_current(
    note_content: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(users_dao.check_auth)],
    db: Session = Depends(get_db),
) -> Union[notes_schema.Note, None]:
    if credentials is not None:
        # При отсутствии доступа check_auth выдаст исключение
        db_user_id = users_dao.get_user_id(db, credentials)

        if db_user_id is not None:
            db_note = notes_dao.create_note(
                db,
                note=notes_schema.NoteCreate(owner_id=db_user_id, content=note_content),
            )
            return db_note
