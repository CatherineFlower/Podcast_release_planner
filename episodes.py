"""Функции для работы с выпусками подкаста."""

from datetime import date

from statuses import get_status_description, is_valid_status


def add_episode(
    episodes: list[dict],
    podcast_id: int,
    title: str,
    topic_id: int,
    status: str,
    release_date: str,
) -> dict:
    """Добавить новый выпуск."""
    if not is_valid_status(status):
        raise ValueError("Недопустимый статус выпуска")

    episode = {
        "id": max((item["id"] for item in episodes), default=0) + 1,
        "podcast_id": podcast_id,
        "title": title,
        "topic_id": topic_id,
        "status": status,
        "release_date": release_date,
    }
    episodes.append(episode)
    return episode


def find_episodes(episodes: list[dict], query: str) -> list[dict]:
    """Найти выпуски по названию."""
    query = query.lower()
    return [
        item
        for item in episodes
        if query in item["title"].lower()
    ]


def iter_episodes_by_status(
    episodes: list[dict],
    status: str,
):
    """Последовательно выдавать выпуски указанного статуса."""
    for episode in episodes:
        if episode["status"] == status:
            yield episode


def filter_by_status(
    episodes: list[dict],
    status: str,
) -> list[dict]:
    """Вернуть выпуски указанного статуса."""
    return list(iter_episodes_by_status(episodes, status))


def sort_by_release_date(episodes: list[dict]) -> list[dict]:
    """Отсортировать выпуски по дате публикации."""
    return sorted(
        episodes,
        key=lambda item: item["release_date"],
    )


def update_status(
    episodes: list[dict],
    episode_id: int,
    status: str,
) -> bool:
    """Изменить статус выпуска."""
    if not is_valid_status(status):
        raise ValueError("Недопустимый статус выпуска")

    for episode in episodes:
        if episode["id"] == episode_id:
            episode["status"] = status
            return True
    return False


def delete_episode(
    episodes: list[dict],
    episode_id: int,
) -> bool:
    """Удалить выпуск по идентификатору."""
    for episode in episodes:
        if episode["id"] == episode_id:
            episodes.remove(episode)
            return True
    return False


def get_statistics(episodes: list[dict]) -> dict[str, int]:
    """Получить количество выпусков по статусам."""
    statistics: dict[str, int] = {}
    for episode in episodes:
        status = episode["status"]
        statistics[status] = statistics.get(status, 0) + 1
    return statistics


def get_days_until_release(release_date: str) -> int:
    """Вернуть число дней до публикации."""
    target_date = date.fromisoformat(release_date)
    return (target_date - date.today()).days


def get_episode_status_text(episode: dict) -> str:
    """Вернуть текстовое описание статуса выпуска."""
    return get_status_description(episode["status"])
