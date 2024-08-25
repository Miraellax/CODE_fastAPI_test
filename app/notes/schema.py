from pydantic import BaseModel


class NoteBase(BaseModel):
    content: str
    owner_id: int


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True
