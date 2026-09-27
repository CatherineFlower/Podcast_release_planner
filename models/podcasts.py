"""Модель подкаста и функции работы с коллекцией."""

from .base import BaseEntity
from .users import Author


class Podcast(BaseEntity):
    """Подкаст компании."""

    def __init__(
        self,
        podcast_id: int,
        title: str,
        description: str,
        author: Author,
    ) -> None:
        super().__init__(podcast_id)
        self.title = title
        self.description = description
        self.author = author

    def __str__(self) -> str:
        return (
            f"#{self.id}: {self.title}\n"
            f"    Автор: {self.author.name}\n"
            f"    Описание: {self.description}"
        )


def add_podcast(
    podcasts: list[Podcast],
    title: str,
    description: str,
    author: Author,
) -> Podcast:
    """Создать подкаст и добавить его в коллекцию."""
    next_id = max((item.id for item in podcasts), default=0) + 1
    podcast = Podcast(next_id, title, description, author)
    podcasts.append(podcast)
    return podcast


def find_podcasts(
    podcasts: list[Podcast],
    query: str,
) -> list[Podcast]:
    """Найти подкасты по названию."""
    query = query.lower()
    return [
        podcast
        for podcast in podcasts
        if query in podcast.title.lower()
    ]


def find_podcast_by_id(
    podcasts: list[Podcast],
    podcast_id: int,
) -> Podcast | None:
    """Найти подкаст по ID."""
    return next(
        (item for item in podcasts if item.id == podcast_id),
        None,
    )
