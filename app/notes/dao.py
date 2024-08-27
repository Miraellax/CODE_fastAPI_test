import asyncio
import json
from typing import List, Type, Dict, Union

import aiohttp as aiohttp
from sqlalchemy.orm import Session

from app.models import models
from app.notes import schema

spellcheck_json_url = "https://speller.yandex.net/services/spellservice.json/checkText"


def get_note(db: Session, note_id: int) -> Union[schema.Note, None]:
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes_by_owner(db: Session, owner_id: int) -> list[Type[schema.Note]]:
    return db.query(models.Note).filter(models.Note.owner_id == owner_id).all()


async def check_text_by_speller(text: str) -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(spellcheck_json_url + "?text=" + text) as resp:
            response = await resp.text()
            json_resp = json.loads(response)
            return json_resp


def correct_text(text: str) -> str:
    speller_result = asyncio.run(check_text_by_speller(text=text))

    for word_dict in speller_result:
        text = (
            text[0 : word_dict["pos"]]
            + word_dict["s"][0]
            + text[word_dict["pos"] + word_dict["len"] :]
        )
    return text


def create_note(db: Session, note: schema.NoteCreate):
    # При проверке текста на ошибки, будут применяться первые предложения Яндекс Спеллера
    note.content = correct_text(note.content)
    db_note = models.Note(owner_id=note.owner_id, content=note.content)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
