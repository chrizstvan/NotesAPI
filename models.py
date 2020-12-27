from pydantic import BaseModel

# request model
class NoteIn(BaseModel):
    title: str
    descriptions: str
    date: str
    completed: bool

#response model
class Note(BaseModel):
    id: int
    title: str
    descriptions: str
    date: str
    completed: bool