"""Сохранение и загрузка JSON."""

import json


def load_episodes(filename: str) -> list[dict]:
    """Загрузить выпуски."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Некорректный формат данных")
            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []


def save_episodes(filename: str, episodes: list[dict]) -> None:
    """Сохранить выпуски."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(episodes, file, ensure_ascii=False, indent=2)
