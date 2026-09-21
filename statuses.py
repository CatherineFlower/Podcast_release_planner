"""Справочник статусов выпусков."""

STATUS_ORDER = (
    "idea",
    "planned",
    "recording",
    "ready",
    "published",
)

VALID_STATUSES = set(STATUS_ORDER)

STATUS_DESCRIPTIONS = {
    "idea": "Идея выпуска",
    "planned": "Выпуск запланирован",
    "recording": "Идет запись",
    "ready": "Выпуск готов к публикации",
    "published": "Выпуск опубликован",
}


def is_valid_status(status: str) -> bool:
    """Проверить, является ли статус допустимым."""
    return status in VALID_STATUSES


def get_status_description(status: str) -> str:
    """Вернуть текстовое описание статуса."""
    return STATUS_DESCRIPTIONS.get(status, "Неизвестный статус")
