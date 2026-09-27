"""Модель выпуска и функции работы с выпусками."""

from .base import BaseEntity
from .podcasts import Podcast
from .statuses import ReleaseStatus
from .topics import Topic
from .users import Author


class Episode(BaseEntity):
    """Выпуск подкаста."""

    def __init__(
        self,
        episode_id: int,
        podcast: Podcast,
        title: str,
        topic: Topic,
        author: Author,
        status: ReleaseStatus,
        release_date: str,
    ) -> None:
        super().__init__(episode_id)
        self.podcast = podcast
        self.title = title
        self.topic = topic
        self.author = author
        self.status = status
        self.release_date = release_date

    def change_status(self, status: ReleaseStatus) -> None:
        """Изменить статус выпуска."""
        self.status = status

    @property
    def is_published(self) -> bool:
        """Опубликован ли выпуск."""
        return self.status == ReleaseStatus.PUBLISHED

    def __str__(self) -> str:
        return (
            f"#{self.id}: {self.title}\n"
            f"    Подкаст: {self.podcast.title}\n"
            f"    Автор: {self.author.name}\n"
            f"    Тема: {self.topic.name}\n"
            f"    Статус: {self.status.title}\n"
            f"    Дата: {self.release_date}"
        )


def add_episode(
    episodes: list[Episode],
    podcast: Podcast,
    title: str,
    topic: Topic,
    author: Author,
    status: ReleaseStatus,
    release_date: str,
) -> Episode:
    """Создать выпуск и добавить его в коллекцию."""
    next_id = max((item.id for item in episodes), default=0) + 1
    episode = Episode(
        next_id,
        podcast,
        title,
        topic,
        author,
        status,
        release_date,
    )
    episodes.append(episode)
    return episode


def find_episodes(
    episodes: list[Episode],
    query: str,
) -> list[Episode]:
    """Найти выпуски по названию, теме или подкасту."""
    query = query.lower()
    return [
        episode
        for episode in episodes
        if (
            query in episode.title.lower()
            or query in episode.topic.name.lower()
            or query in episode.podcast.title.lower()
        )
    ]


def find_episode_by_id(
    episodes: list[Episode],
    episode_id: int,
) -> Episode | None:
    """Найти выпуск по ID."""
    return next(
        (item for item in episodes if item.id == episode_id),
        None,
    )


def filter_by_status(
    episodes: list[Episode],
    status: ReleaseStatus,
) -> list[Episode]:
    """Отобрать выпуски по статусу."""
    return [item for item in episodes if item.status == status]


def sort_by_release_date(
    episodes: list[Episode],
) -> list[Episode]:
    """Отсортировать выпуски по дате."""
    return sorted(episodes, key=lambda item: item.release_date)


def delete_episode(
    episodes: list[Episode],
    episode_id: int,
) -> bool:
    """Удалить выпуск по ID."""
    episode = find_episode_by_id(episodes, episode_id)
    if episode is None:
        return False
    episodes.remove(episode)
    return True
