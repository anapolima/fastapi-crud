from fastapi import APIRouter, HTTPException
from typing import List

from app.api import crud
from app.api.models import NoteDB, NoteSchema

router = APIRouter()

@router.post("/", response_model=NoteDB, status_code=201)
async def createNote(payload: NoteSchema):
    note_id = await crud.post(payload)

    responseObject = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }

    return responseObject

@router.get("/{id}/", response_model=NoteDB)
async def readNote(id: int):
    note = await crud.get(id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@router.get("/", response_model=List[NoteDB])
async def readAllNotes():
    return await crud.getAll()

@router.put("/{id}/", response_model=NoteDB)
async def updateNote(id: int, payload: NoteSchema):
    note = await crud.get(id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    noteId = await crud.put(id, payload)

    responseObject = {
        "id": noteId,
        "title": payload.title,
        "description": payload.description,
    }
    return responseObject

@router.delete("/{id}/", response_model=NoteDB)
async def deleteNote(id: int):
    note = await crud.get(id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note
