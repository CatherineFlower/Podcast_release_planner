"""Статусы подготовки выпуска."""

from enum import Enum


class ReleaseStatus(str, Enum):
    """Допустимые статусы выпуска."""

    IDEA = "idea"
    PLANNED = "planned"
    RECORDING = "recording"
    READY = "ready"
    PUBLISHED = "published"

    @property
    def title(self) -> str:
        """Человекочитаемое название статуса."""
        titles = {
            ReleaseStatus.IDEA: "Идея",
            ReleaseStatus.PLANNED: "Запланирован",
            ReleaseStatus.RECORDING: "Идет запись",
            ReleaseStatus.READY: "Готов к публикации",
            ReleaseStatus.PUBLISHED: "Опубликован",
        }
        return titles[self]

    @classmethod
    def from_value(cls, value: str) -> "ReleaseStatus":
        """Создать статус из строкового значения."""
        return cls(value)

    @staticmethod
    def values() -> tuple[str, ...]:
        """Вернуть допустимые значения статусов."""
        return tuple(status.value for status in ReleaseStatus)
