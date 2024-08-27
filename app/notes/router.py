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


# curl -X "POST" "http://127.0.0.1:8000/notes/post/{owner_id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"content\": \"hepl me\", \"owner_id\": 1}" --user "first:111"
# out -> {"content":"help me","owner_id":1,"id":7}
