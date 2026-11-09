"""Создание таблиц SQLite из sql/schema.sql."""

from pathlib import Path

from .database import BASE_DIR, DB_PATH, get_connection

SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def main() -> None:
    """Создать файл базы и выполнить схему повторно-безопасно."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_FILE.read_text(encoding="utf-8")

    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()

    print(f"База готова: {DB_PATH}")


if __name__ == "__main__":
    main()
