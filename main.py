"""Консольная система планирования выпусков подкаста."""

from episodes import (
    add_episode,
    delete_episode,
    filter_by_status,
    find_episodes,
    get_episode_status_text,
    get_statistics,
    sort_by_release_date,
    update_status,
)
from podcasts import (
    add_podcast,
    podcast_exists,
    sort_podcasts_by_title,
)
from storage import load_json, save_json
from topics import add_topic, topic_exists
from utils import input_date, input_int, input_status

PODCASTS_FILE = "data/podcasts.json"
EPISODES_FILE = "data/episodes.json"
TOPICS_FILE = "data/topics.json"


def show_podcasts(podcasts: list[dict]) -> None:
    """Вывести список подкастов."""
    if not podcasts:
        print("Подкасты не найдены.")
        return

    for podcast in podcasts:
        print(
            f'#{podcast["id"]}: {podcast["title"]} — '
            f'{podcast["description"]}'
        )


def show_topics(topics: list[dict]) -> None:
    """Вывести список тем."""
    if not topics:
        print("Темы не найдены.")
        return

    for topic in topics:
        print(f'#{topic["id"]}: {topic["name"]}')


def show_episodes(episodes: list[dict]) -> None:
    """Вывести список выпусков."""
    if not episodes:
        print("Выпуски не найдены.")
        return

    for episode in episodes:
        print(
            f'#{episode["id"]}: {episode["title"]} | '
            f'подкаст #{episode["podcast_id"]} | '
            f'тема #{episode["topic_id"]} | '
            f'{get_episode_status_text(episode)} | '
            f'{episode["release_date"]}'
        )


def save_all(
    podcasts: list[dict],
    episodes: list[dict],
    topics: list[dict],
) -> None:
    """Сохранить все данные проекта."""
    save_json(PODCASTS_FILE, podcasts)
    save_json(EPISODES_FILE, episodes)
    save_json(TOPICS_FILE, topics)


def main() -> None:
    """Запустить консольное меню."""
    podcasts = load_json(PODCASTS_FILE)
    episodes = load_json(EPISODES_FILE)
    topics = load_json(TOPICS_FILE)

    while True:
        print("\n=== Планировщик выпусков подкаста ===")
        print("1. Показать подкасты")
        print("2. Добавить подкаст")
        print("3. Показать темы")
        print("4. Добавить тему")
        print("5. Показать выпуски")
        print("6. Добавить выпуск")
        print("7. Найти выпуск")
        print("8. Изменить статус")
        print("9. Удалить выпуск")
        print("10. Фильтр по статусу")
        print("11. Сортировка по дате")
        print("12. Статистика")
        # print("13. Интроспекция данных")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_podcasts(sort_podcasts_by_title(podcasts))

        elif choice == "2":
            title = input("Название подкаста: ").strip()
            description = input("Описание: ").strip()
            add_podcast(podcasts, title, description)
            save_all(podcasts, episodes, topics)
            print("Подкаст добавлен.")

        elif choice == "3":
            show_topics(topics)

        elif choice == "4":
            name = input("Название темы: ").strip()
            add_topic(topics, name)
            save_all(podcasts, episodes, topics)
            print("Тема добавлена.")

        elif choice == "5":
            show_episodes(episodes)

        elif choice == "6":
            podcast_id = input_int("ID подкаста: ")
            if not podcast_exists(podcasts, podcast_id):
                print("Подкаст не найден.")
                continue

            topic_id = input_int("ID темы: ")
            if not topic_exists(topics, topic_id):
                print("Тема не найдена.")
                continue

            title = input("Название выпуска: ").strip()
            status = input_status("Статус: ")
            release_date = input_date("Дата (ГГГГ-ММ-ДД): ")

            add_episode(
                episodes,
                podcast_id,
                title,
                topic_id,
                status,
                release_date,
            )
            save_all(podcasts, episodes, topics)
            print("Выпуск добавлен.")

        elif choice == "7":
            query = input("Название выпуска: ").strip()
            show_episodes(find_episodes(episodes, query))

        elif choice == "8":
            episode_id = input_int("ID выпуска: ")
            status = input_status("Новый статус: ")
            if update_status(episodes, episode_id, status):
                save_all(podcasts, episodes, topics)
                print("Статус изменен.")
            else:
                print("Выпуск не найден.")

        elif choice == "9":
            episode_id = input_int("ID выпуска: ")
            if delete_episode(episodes, episode_id):
                save_all(podcasts, episodes, topics)
                print("Выпуск удален.")
            else:
                print("Выпуск не найден.")

        elif choice == "10":
            status = input_status("Статус: ")
            show_episodes(filter_by_status(episodes, status))

        elif choice == "11":
            show_episodes(sort_by_release_date(episodes))

        elif choice == "12":
            print("Всего выпусков:", len(episodes))
            for status, count in get_statistics(episodes).items():
                print(f"{status}: {count}")

        # elif choice == "13":
        #     info = describe_object(episodes)
        #     print("Тип:", info["type"])
        #     print("Класс:", info["class"])
        #     print("Поддерживает итерацию:", info["has_iter"])
        #     print("Публичные атрибуты:", info["public_attributes"])

        elif choice == "0":
            save_all(podcasts, episodes, topics)
            print("Данные сохранены.")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
