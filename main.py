from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database_setup import DATABASE_URL, notes, database
from models import Note, NoteIn

app = FastAPI(title='Notes API')
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credential=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# setup database even

@app.on_event("startup")
async def starup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(
        title = note.title,
        descriptions = note.descriptions,
        date = note.date,
        completed = note.completed
    )

    last_record_id = await database.execute(query)
    return {** note.dict(), "id": last_record_id}


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.get("/notes/{note_id}", response_model=Note)
async def read_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(
        title = payload.title,
        descriptions = payload.descriptions,
        date = payload.date,
        completed = payload.completed
    )

    await database.execute(query)
    return {** payload.dict(), "id": note_id}


@app.delete("/notes/{notes_id}")
async def delete_note(notes_id: int):
    query = notes.delete().where(notes.c.id == notes_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully".format(notes_id)}
