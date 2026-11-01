"""Однократный перенос исходных данных ПР1-ПР6 из JSON в SQLite."""

import json
from pathlib import Path

from .database import BASE_DIR, get_connection

DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
TOPICS_FILE = DATA_DIR / "topics.json"
PODCASTS_FILE = DATA_DIR / "podcasts.json"
EPISODES_FILE = DATA_DIR / "episodes.json"


def load_json(filename: Path) -> list[dict]:
    """Прочитать JSON-массив."""
    with filename.open(encoding="utf-8") as file:
        return json.load(file)


def import_users(conn) -> None:
    """Импортировать пользователей первыми: на них ссылаются подкасты."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (
            id, name, login, password_hash, role
        ) VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["name"],
                item["login"],
                item["password_hash"],
                item["role"],
            )
            for item in users
        ],
    )


def import_topics(conn) -> None:
    """Импортировать темы."""
    topics = load_json(TOPICS_FILE)
    conn.executemany(
        "INSERT INTO topics (id, name) VALUES (?, ?)",
        [(item["id"], item["name"]) for item in topics],
    )


def import_podcasts(conn) -> None:
    """Импортировать подкасты после пользователей."""
    podcasts = load_json(PODCASTS_FILE)
    conn.executemany(
        """
        INSERT INTO podcasts (
            id, title, description, author_id
        ) VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["title"],
                item["description"],
                item["author_id"],
            )
            for item in podcasts
        ],
    )


def import_episodes(conn) -> None:
    """Импортировать выпуски последними из-за трёх внешних ключей."""
    episodes = load_json(EPISODES_FILE)
    conn.executemany(
        """
        INSERT INTO episodes (
            id, podcast_id, title, topic_id,
            author_id, status, release_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["podcast_id"],
                item["title"],
                item["topic_id"],
                item["author_id"],
                item["status"],
                item["release_date"],
            )
            for item in episodes
        ],
    )


def clear_tables(conn) -> None:
    """Очистить таблицы в порядке, обратном зависимостям."""
    conn.execute("DELETE FROM episodes")
    conn.execute("DELETE FROM podcasts")
    conn.execute("DELETE FROM topics")
    conn.execute("DELETE FROM users")


def main() -> None:
    """Импортировать все исходные JSON-данные одной транзакцией."""
    conn = get_connection()
    try:
        clear_tables(conn)
        import_users(conn)
        import_topics(conn)
        import_podcasts(conn)
        import_episodes(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print("JSON-данные перенесены в SQLite.")


if __name__ == "__main__":
    main()
