from fastapi.testclient import TestClient
from mbb_agent.app import app

client = TestClient(app)

def test_memory_requires_session_id():
    r = client.get("/memory")
    assert r.status_code == 422

def test_chat_and_memory_roundtrip():
    r = client.post("/chat", json={"session_id": "ci", "user_message": "hello"})
    assert r.status_code == 200

    r2 = client.get("/memory", params={"session_id": "ci"})
    assert r2.status_code == 200
    data = r2.json()
    assert any(e.get("role") == "user" and e.get("content") == "hello" for e in data)
