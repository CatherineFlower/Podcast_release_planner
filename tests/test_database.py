"""Проверки слоя SQLite ПР7."""

import json
from pathlib import Path

from db.database import BASE_DIR, get_connection


def test_database_tables_exist():
    conn = get_connection()
    try:
        names = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    finally:
        conn.close()
    assert {"users", "topics", "podcasts", "episodes"} <= names


def test_foreign_keys_enabled():
    conn = get_connection()
    try:
        enabled = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        episode_keys = conn.execute(
            "PRAGMA foreign_key_list(episodes)"
        ).fetchall()
    finally:
        conn.close()
    assert enabled == 1
    assert len(episode_keys) == 3


def test_imported_counts_match_json():
    sources = [
        ("users.json", "SELECT COUNT(*) FROM users"),
        ("topics.json", "SELECT COUNT(*) FROM topics"),
        ("podcasts.json", "SELECT COUNT(*) FROM podcasts"),
        ("episodes.json", "SELECT COUNT(*) FROM episodes"),
    ]
    conn = get_connection()
    try:
        for filename, query in sources:
            data = json.loads(
                (BASE_DIR / "data" / filename).read_text(encoding="utf-8")
            )
            count = conn.execute(query).fetchone()[0]
            assert count == len(data)
    finally:
        conn.close()
