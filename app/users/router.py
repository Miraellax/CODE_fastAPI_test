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


@router.get("/current")
def read_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(check_auth)]
) -> Dict:
    if credentials is not None:
        return {"username": credentials.username, "password": credentials.password}


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
