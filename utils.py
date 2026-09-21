"""Вспомогательные функции пользовательского ввода."""

from datetime import datetime

from statuses import STATUS_ORDER, is_valid_status


def input_int(prompt: str) -> int:
    """Запросить целое число с обработкой ошибки."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Используйте формат ГГГГ-ММ-ДД.")


def input_status(prompt: str) -> str:
    """Запросить допустимый статус выпуска."""
    print("Доступные статусы:", ", ".join(STATUS_ORDER))

    while True:
        value = input(prompt).strip().lower()
        if is_valid_status(value):
            return value
        print("Некорректный статус. Попробуйте еще раз.")


# def describe_object(value: object) -> dict[str, object]:
#     """Вернуть сведения об объекте средствами интроспекции."""
#     return {
#         "type": type(value).__name__,
#         "class": value.__class__.__name__,
#         "has_iter": hasattr(value, "__iter__"),
#         "public_attributes": [
#             name for name in dir(value) if not name.startswith("_")
#         ],
#     }
