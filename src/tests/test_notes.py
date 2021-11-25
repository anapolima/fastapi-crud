import json
import pytest
from app.api import crud

def testCreateNote(test_app, monkeypatch):
    testRequestPayload = {"title": "something", "description": "something else"}
    testResponsePayload = {"id": 1, "title": "something", "description": "something else"}

    async def mockPost(payload):
        return 1

    monkeypatch.setattr(crud, "post", mockPost)

    response = test_app.post("/notes/", data=json.dumps(testRequestPayload),)

    assert response.status_code == 201
    assert response.json() == testResponsePayload

def testCreateNoteInvalidJson(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422

def testReadNote(test_app, monkeypatch):
    testData = {"id": 1, "title": "something", "description": "something else"}

    async def mockGet(id):
        return testData

    monkeypatch.setattr(crud, "get", mockGet)

    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == testData

def testReadNoteIncorrectId(test_app, monkeypatch):
    async def mockGet(id):
        return None

    monkeypatch.setattr(crud, "get", mockGet)

    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def testUpdateNote(test_app, monkeypatch):
    testUpdateData = {"title": "someone", "description": "someone else", "id": 1}

    async def mockGet(id):
        return True

    monkeypatch.setattr(crud, "get", mockGet)

    async def mockPut(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mockPut)

    response = test_app.put("/notes/1/", data=json.dumps(testUpdateData))
    assert response.status_code == 200
    assert response.json() == testUpdateData

@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
    ],
)

def testUpdateNoteInvalid(test_app, monkeypatch, id, payload, status_code):
    async def mockGet(id):
        return None

    monkeypatch.setattr(crud, "get", mockGet)

    response = test_app.put(f"/notes/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code

def testRemoveNote(test_app, monkeypatch):
    testData = {"title": "something", "description": "something else", "id": 1}

    async def mockGet(id):
        return testData

    monkeypatch.setattr(crud, "get", mockGet)

    async def mockDelete(id):
        return id

    monkeypatch.setattr(crud, "delete", mockDelete)

    response = test_app.delete("/notes/1/")
    assert response.status_code == 200
    assert response.json() == testData

def testRemoveNoteIncorrectId(test_app, monkeypatch):
    async def mockGet(id):
        return None

    monkeypatch.setattr(crud, "get", mockGet)

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"