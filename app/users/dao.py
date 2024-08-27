from typing import Union, Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import models
from app.users import schema as user_schema


security = HTTPBasic()


def check_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> HTTPBasicCredentials:

    db_user = (
        db.query(models.User)
        .filter(
            models.User.username == credentials.username
            and models.User.password == credentials.password
        )
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials


def get_user_by_note_id(db: Session, note_id: int) -> Union[user_schema.User, None]:
    return db.query(models.User).filter(models.User.id == note_id).first()


def get_user_id(db: Session, credentials: HTTPBasicCredentials) -> Union[int, None]:
    user = (
        db.query(models.User)
        .filter(
            models.User.username == credentials.username
            and models.User.password == credentials.password
        )
        .first()
    )
    if user is not None:
        return user.id
    return
