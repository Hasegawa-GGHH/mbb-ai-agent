from __future__ import annotations

import os
from functools import lru_cache

from .storage import Storage

@lru_cache(maxsize=1)
def get_settings() -> dict:
    # まずは最小：環境変数でDBパスを差し替え可能にする
    db_path = os.getenv("MBB_DB_PATH", "data/mbb.db")
    return {"db_path": db_path}

def get_storage() -> Storage:
    s = get_settings()
    return Storage(db_path=s["db_path"])

