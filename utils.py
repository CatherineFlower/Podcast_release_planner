"""Вспомогательные функции ввода."""

from datetime import datetime

from models.statuses import ReleaseStatus


def input_int(prompt: str) -> int:
    """Запросить целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_text(prompt: str) -> str:
    """Запросить непустую строку, корректную для UTF-8."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Поле не должно быть пустым.")
            continue
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            print("Некорректные символы. Введите текст заново.")
            continue
        return value


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input_text(prompt)
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Используйте формат ГГГГ-ММ-ДД.")


def input_status(prompt: str) -> ReleaseStatus:
    """Запросить допустимый статус."""
    print("Доступные статусы:")
    for status in ReleaseStatus:
        print(f"- {status.value}: {status.title}")

    while True:
        value = input_text(prompt).lower()
        try:
            return ReleaseStatus.from_value(value)
        except ValueError:
            print("Некорректный статус.")
