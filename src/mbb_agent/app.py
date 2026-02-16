from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .storage import append_event, get_recent_events

app = FastAPI(title="MBB Agent Phase0")

class ChatIn(BaseModel):
    session_id: str
    user_message: str

class ChatOut(BaseModel):
    session_id: str
    assistant_message: str
    recent_events: List[dict]

def toy_reply(user_message: str) -> str:
    return f"記録しました: {user_message}"

@app.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn):
    append_event(payload.session_id, "user", payload.user_message)
    assistant = toy_reply(payload.user_message)
    append_event(payload.session_id, "assistant", assistant)
    events = get_recent_events(payload.session_id)
    return ChatOut(
        session_id=payload.session_id,
        assistant_message=assistant,
        recent_events=events
    )

@app.get("/memory")
def memory(session_id: str):
    return get_recent_events(session_id)
