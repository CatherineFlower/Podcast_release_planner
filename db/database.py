"""Подключение к SQLite для ПР7 без Django ORM."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "podcast_planner.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с SQLite и включить внешние ключи."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
