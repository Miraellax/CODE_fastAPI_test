from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.notes import schema, dao
from app.notes.schema import NoteBase, NoteCreate, Note

router = APIRouter(prefix='/notes')

# @router.post("/add/")
# async def add_note(note: NoteCreate) -> dict:
#     check = await MajorsDAO.add(**major.dict())
#     if check:
#         return {"message": "Факультет успешно добавлен!", "major": major}
#     else:
#         return {"message": "Ошибка при добавлении факультета!"}

# @app.get('/stock/{symbol}', response_model=schemas.Stock, status_code=200)
# def get_stock(symbol: str, db: Session = Depends(get_db)) -> models.Stock:
#     db_stock = crud.get_stock(db, symbol=symbol)
#     if db_stock is None:
#         raise HTTPException(
#             status_code=404, detail=f"No stock {symbol} found."
#         )
#
#     return db_stock

@router.get("/{note_id}", response_model=schema.Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = dao.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note is not found")
    return db_note




# @router.post("/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await database.execute(query)
#     return {**note.dict(), "id": last_record_id}