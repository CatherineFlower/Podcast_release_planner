"""Функции безопасного ввода."""

from datetime import datetime

STATUSES = {"idea", "planned", "recording", "ready", "published"}


def input_int(prompt: str) -> int:
    """Запросить целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> str:
    """Запросить дату ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Используйте формат ГГГГ-ММ-ДД.")


def input_status(prompt: str) -> str:
    """Запросить допустимый статус."""
    print("Доступные статусы: idea, planned, recording, ready, published.")

    while True:
        value = input(prompt).strip().lower()

        if value in STATUSES:
            return value

        print("Некорректный статус. Попробуйте еще раз.")
