"""Функции для работы с выпусками подкаста."""


def add_episode(episodes: list[dict], title: str, topic: str,
                status: str, release_date: str) -> dict:
    """Добавить новый выпуск."""
    episode = {
        "id": max((item["id"] for item in episodes), default=0) + 1,
        "title": title,
        "topic": topic,
        "status": status,
        "release_date": release_date,
    }
    episodes.append(episode)
    return episode


def find_episodes(episodes: list[dict], query: str) -> list[dict]:
    """Найти выпуски по названию или теме."""
    query = query.lower()
    return [
        item for item in episodes
        if query in item["title"].lower() or query in item["topic"].lower()
    ]


def filter_by_status(episodes: list[dict], status: str) -> list[dict]:
    """Отобрать выпуски по статусу."""
    return [item for item in episodes if item["status"] == status]


def sort_by_release_date(episodes: list[dict]) -> list[dict]:
    """Отсортировать выпуски по дате."""
    return sorted(episodes, key=lambda item: item["release_date"])


def update_status(episodes: list[dict], episode_id: int, status: str) -> bool:
    """Изменить статус выпуска."""
    for item in episodes:
        if item["id"] == episode_id:
            item["status"] = status
            return True
    return False


def delete_episode(episodes: list[dict], episode_id: int) -> bool:
    """Удалить выпуск."""
    for item in episodes:
        if item["id"] == episode_id:
            episodes.remove(item)
            return True
    return False


def get_status_description(status: str) -> str:
    """Вернуть текстовое описание статуса (логика из ПР1)."""
    descriptions = {
        "idea": "Идея выпуска",
        "planned": "Выпуск запланирован",
        "recording": "Идет запись",
        "ready": "Выпуск готов к публикации",
        "published": "Выпуск опубликован",
    }
    return descriptions.get(status, "Неизвестный статус")


def get_statistics(episodes: list[dict]) -> dict[str, int]:
    """Получить статистику по статусам."""
    result: dict[str, int] = {}
    for item in episodes:
        status = item["status"]
        result[status] = result.get(status, 0) + 1
    return result
