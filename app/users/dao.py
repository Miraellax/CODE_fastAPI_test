from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.notes import schema as note_schema
from app.users import schema as user_schema

router = APIRouter(prefix='/user')

# # TODO подумать как юзера не по айди вызывать, а по аутентификации
# @router.get("/{user_id}/notes", response_model=schema.Note)
# def read_note(note_id: int, db: Session = Depends(get_db)):
#     db_note = dao.get_note(db, note_id=note_id)
#     if db_note is None:
#         raise HTTPException(status_code=404, detail="Note is not found")
#     return db_note
