import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path("data") / "mbb.db"

def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def append_event(session_id: str, role: str, content: str) -> None:
    conn = _conn()
    conn.execute(
        "INSERT INTO events(session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content),
    )
    conn.commit()
    conn.close()

def get_recent_events(session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    conn = _conn()
    cur = conn.execute(
        "SELECT role, content, created_at FROM events WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    rows.reverse()
    return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]


class Storage:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

    def _conn(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn

    def append_event(self, session_id: str, role: str, content: str) -> None:
        conn = self._conn()
        conn.execute(
            "INSERT INTO events(session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )
        conn.commit()
        conn.close()

    def get_recent_events(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        conn = self._conn()
        cur = conn.execute(
            "SELECT role, content, created_at FROM events WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        )
        rows = cur.fetchall()
        conn.close()
        rows.reverse()
        return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]
