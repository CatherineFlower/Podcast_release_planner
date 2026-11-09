"""Перенос данных ПР7 из SQLite в таблицы, управляемые Django ORM."""

import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "podcast_planner.sqlite"
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "podcast_planner.settings")
django.setup()

from authors_web.models import User  # noqa: E402
from episodes_web.models import Episode  # noqa: E402
from podcasts_web.models import Podcast  # noqa: E402
from topics_web.models import Topic  # noqa: E402


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        users = connection.execute(
            "SELECT id, name, login, password_hash, role FROM users ORDER BY id"
        ).fetchall()
        topics = connection.execute(
            "SELECT id, name FROM topics ORDER BY id"
        ).fetchall()
        podcasts = connection.execute(
            "SELECT id, title, description, author_id FROM podcasts ORDER BY id"
        ).fetchall()
        episodes = connection.execute(
            "SELECT id, podcast_id, title, topic_id, author_id, status, release_date "
            "FROM episodes ORDER BY id"
        ).fetchall()

    with transaction.atomic():
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "login": row["login"],
                    "password_hash": row["password_hash"],
                    "role": row["role"],
                },
            )
        for row in topics:
            Topic.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )
        for row in podcasts:
            Podcast.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "title": row["title"],
                    "description": row["description"],
                    "author_id": row["author_id"],
                },
            )
        for row in episodes:
            Episode.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "podcast_id": row["podcast_id"],
                    "title": row["title"],
                    "topic_id": row["topic_id"],
                    "author_id": row["author_id"],
                    "status": row["status"],
                    "release_date": date.fromisoformat(row["release_date"]),
                },
            )

    print("Перенос завершён:")
    print(" users:", User.objects.count())
    print(" topics:", Topic.objects.count())
    print(" podcasts:", Podcast.objects.count())
    print(" episodes:", Episode.objects.count())


if __name__ == "__main__":
    main()
