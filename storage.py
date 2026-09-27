"""Загрузка и сохранение объектной модели в JSON."""

import json
from pathlib import Path

from models import Author, Episode, Podcast, ReleaseStatus, Topic, User


def _read_json(filename: str) -> list[dict]:
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        raise ValueError("JSON-файл должен содержать список.")
    return data


def _write_json(filename: str, data: list[dict]) -> None:
    """Безопасно записать данные через временный файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    temp_path.replace(path)


def load_users(filename: str) -> list[User]:
    return [User.from_data(item) for item in _read_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    data = [
        {
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "password_hash": user.password_hash,
            "role": user.role,
        }
        for user in users
    ]
    _write_json(filename, data)


def load_topics(filename: str) -> list[Topic]:
    return [
        Topic(item["id"], item["name"])
        for item in _read_json(filename)
    ]


def save_topics(filename: str, topics: list[Topic]) -> None:
    data = [{"id": item.id, "name": item.name} for item in topics]
    _write_json(filename, data)


def load_podcasts(
    filename: str,
    users: list[User],
) -> list[Podcast]:
    authors = {
        user.id: user
        for user in users
        if isinstance(user, Author)
    }
    result: list[Podcast] = []

    for item in _read_json(filename):
        author = authors.get(item["author_id"])
        if author is None:
            continue
        result.append(
            Podcast(
                item["id"],
                item["title"],
                item["description"],
                author,
            )
        )
    return result


def save_podcasts(
    filename: str,
    podcasts: list[Podcast],
) -> None:
    data = [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "author_id": item.author.id,
        }
        for item in podcasts
    ]
    _write_json(filename, data)


def load_episodes(
    filename: str,
    podcasts: list[Podcast],
    topics: list[Topic],
    users: list[User],
) -> list[Episode]:
    podcast_map = {item.id: item for item in podcasts}
    topic_map = {item.id: item for item in topics}
    author_map = {
        user.id: user
        for user in users
        if isinstance(user, Author)
    }

    result: list[Episode] = []
    for item in _read_json(filename):
        podcast = podcast_map.get(item["podcast_id"])
        topic = topic_map.get(item["topic_id"])
        author = author_map.get(item["author_id"])
        if podcast is None or topic is None or author is None:
            continue

        result.append(
            Episode(
                item["id"],
                podcast,
                item["title"],
                topic,
                author,
                ReleaseStatus.from_value(item["status"]),
                item["release_date"],
            )
        )
    return result


def save_episodes(
    filename: str,
    episodes: list[Episode],
) -> None:
    data = [
        {
            "id": item.id,
            "podcast_id": item.podcast.id,
            "title": item.title,
            "topic_id": item.topic.id,
            "author_id": item.author.id,
            "status": item.status.value,
            "release_date": item.release_date,
        }
        for item in episodes
    ]
    _write_json(filename, data)
