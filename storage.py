"""Загрузка и сохранение данных проекта в JSON."""

import json
from pathlib import Path


def load_json(filename: str) -> list[dict]:
    """Загрузить список словарей из JSON-файла."""
    path = Path(filename)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        raise ValueError("JSON-файл должен содержать список")
    return data


def save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
