"""Модель темы выпуска."""

from .base import BaseEntity


class Topic(BaseEntity):
    """Тема выпуска."""

    def __init__(self, topic_id: int, name: str) -> None:
        super().__init__(topic_id)
        self.name = name

    def __str__(self) -> str:
        return f"#{self.id}: {self.name}"
