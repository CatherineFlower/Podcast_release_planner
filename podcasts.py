"""Функции для работы с подкастами."""


def add_podcast(
    podcasts: list[dict],
    title: str,
    description: str,
) -> dict:
    """Добавить подкаст в список."""
    podcast = {
        "id": max((item["id"] for item in podcasts), default=0) + 1,
        "title": title,
        "description": description,
    }
    podcasts.append(podcast)
    return podcast


def find_podcasts(podcasts: list[dict], query: str) -> list[dict]:
    """Найти подкасты по названию."""
    query = query.lower()
    return [
        item
        for item in podcasts
        if query in item["title"].lower()
    ]


def sort_podcasts_by_title(podcasts: list[dict]) -> list[dict]:
    """Вернуть подкасты, отсортированные по названию."""
    return sorted(podcasts, key=lambda item: item["title"].lower())


def podcast_exists(podcasts: list[dict], podcast_id: int) -> bool:
    """Проверить существование подкаста по идентификатору."""
    return any(item["id"] == podcast_id for item in podcasts)
