"""Система планирования выпусков подкаста."""

from episodes import (
    add_episode, delete_episode, filter_by_status, find_episodes,
    get_statistics, get_status_description, sort_by_release_date,
    update_status,
)
from storage import load_episodes, save_episodes
from utils import input_date, input_int, input_status

DATA_FILE = "data/episodes.json"


def show_episodes(episodes: list[dict]) -> None:
    """Вывести список выпусков."""
    if not episodes:
        print("Выпуски не найдены.")
        return
    for item in episodes:
        print(
            f'#{item["id"]}: {item["title"]} | {item["topic"]} | '
            f'{get_status_description(item["status"])} | '
            f'{item["release_date"]}'
        )


def main() -> None:
    """Запустить консольное меню."""
    episodes = load_episodes(DATA_FILE)
    while True:
        print("\n=== Планировщик выпусков подкаста ===")
        print("1. Показать выпуски")
        print("2. Добавить выпуск")
        print("3. Найти выпуск")
        print("4. Изменить статус")
        print("5. Удалить выпуск")
        print("6. Фильтр по статусу")
        print("7. Сортировка по дате")
        print("8. Статистика")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_episodes(episodes)
        elif choice == "2":
            title = input("Название: ").strip()
            topic = input("Тема: ").strip()
            status = input_status("Статус: ")
            release_date = input_date("Дата (ГГГГ-ММ-ДД): ")
            add_episode(episodes, title, topic, status, release_date)
            save_episodes(DATA_FILE, episodes)
            print("Выпуск добавлен.")
        elif choice == "3":
            query = input("Название или тема: ").strip()
            show_episodes(find_episodes(episodes, query))
        elif choice == "4":
            episode_id = input_int("ID выпуска: ")
            status = input_status("Новый статус: ")
            if update_status(episodes, episode_id, status):
                save_episodes(DATA_FILE, episodes)
                print("Статус изменен.")
            else:
                print("Выпуск не найден.")
        elif choice == "5":
            episode_id = input_int("ID выпуска: ")
            if delete_episode(episodes, episode_id):
                save_episodes(DATA_FILE, episodes)
                print("Выпуск удален.")
            else:
                print("Выпуск не найден.")
        elif choice == "6":
            show_episodes(filter_by_status(
                episodes, input_status("Статус: ")
            ))
        elif choice == "7":
            show_episodes(sort_by_release_date(episodes))
        elif choice == "8":
            print("Всего выпусков:", len(episodes))
            for status, count in get_statistics(episodes).items():
                print(f"{status}: {count}")
        elif choice == "0":
            save_episodes(DATA_FILE, episodes)
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
