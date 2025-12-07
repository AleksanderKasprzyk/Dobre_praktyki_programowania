from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent / "queue.sqlite3"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL)""")
        conn.commit()


def add_task(status: str = "pending") -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO tasks(status) VALUES (?)", (status,))
        conn.commit()
        return cur.lastrowid


def get_next_pending():
    with get_conn() as conn:
        cur = conn.execute("SELECT id, status FROM tasks " "WHERE status = 'pending' "
            "ORDER BY id LIMIT 1")
        row = cur.fetchone()
        return row


def update_status(task_id: int, new_status: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()


if __name__ == "__main__":
    init_db()
    print("Baza queue.sqlite3 gotowa.")
