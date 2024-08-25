from fastapi import APIRouter
from app.users.schema import UserBase, UserCreate

router = APIRouter(prefix='/users')


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