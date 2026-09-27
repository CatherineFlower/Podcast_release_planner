"""Базовые классы проекта."""


class BaseEntity:
    """Базовая сущность с идентификатором."""

    def __init__(self, entity_id: int) -> None:
        self.id = entity_id

    def __str__(self) -> str:
        return f"#{self.id}"
