"""Короткая проверка структуры и данных SQLite перед защитой."""

from .database import DB_PATH, get_connection


def main() -> None:
    """Показать путь, таблицы, количество записей и внешние ключи."""
    conn = get_connection()
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' ORDER BY name"
        ).fetchall()

        print(f"База: {DB_PATH}")
        print("Таблицы:", ", ".join(row["name"] for row in tables))

        for table in ("users", "topics", "podcasts", "episodes"):
            count = conn.execute(
                "SELECT COUNT(*) AS count FROM " + table
            ).fetchone()["count"]
            print(f"{table}: {count}")

        print("Внешние ключи episodes:")
        for row in conn.execute(
            "PRAGMA foreign_key_list(episodes)"
        ).fetchall():
            print(
                f"  {row['from']} -> {row['table']}.{row['to']}"
            )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
