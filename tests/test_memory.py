from fastapi.testclient import TestClient

from mbb_agent.app import app
from mbb_agent.dependencies import get_storage
from mbb_agent.storage import Storage

def make_client(tmp_path):
    test_db = tmp_path / "test.db"

    def override_get_storage():
        return Storage(db_path=str(test_db))

    app.dependency_overrides[get_storage] = override_get_storage
    return TestClient(app)

def test_memory_requires_session_id(tmp_path):
    client = make_client(tmp_path)
    r = client.get("/memory")
    assert r.status_code == 422

def test_chat_and_memory_roundtrip(tmp_path):
    client = make_client(tmp_path)

    r = client.post("/chat", json={"session_id": "ci", "user_message": "hello"})
    assert r.status_code == 200

    r2 = client.get("/memory", params={"session_id": "ci"})
    assert r2.status_code == 200
    data = r2.json()
    assert any(e.get("role") == "user" and e.get("content") == "hello" for e in data)
