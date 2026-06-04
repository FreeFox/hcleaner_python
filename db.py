import sqlite3
from pathlib import Path

DB_PATH = Path("sessions/queue.db")

_conn: sqlite3.Connection | None = None


def init() -> None:
    global _conn
    _conn = sqlite3.connect(DB_PATH)
    _conn.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            message_id INTEGER NOT NULL,
            chat_id    INTEGER NOT NULL,
            date       TEXT    NOT NULL,
            PRIMARY KEY (message_id, chat_id)
        )
    """)
    _conn.commit()


def add(message_id: int, chat_id: int, date: str) -> None:
    _conn.execute(
        "INSERT OR IGNORE INTO queue (message_id, chat_id, date) VALUES (?, ?, ?)",
        (message_id, chat_id, date),
    )
    _conn.commit()


def remove(message_id: int, chat_id: int) -> None:
    _conn.execute(
        "DELETE FROM queue WHERE message_id = ? AND chat_id = ?",
        (message_id, chat_id),
    )
    _conn.commit()


def load_all() -> list[dict]:
    rows = _conn.execute("SELECT message_id, chat_id, date FROM queue").fetchall()
    return [{"message": r[0], "chat": r[1], "date": r[2]} for r in rows]
