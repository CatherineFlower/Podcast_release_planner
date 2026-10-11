"""Система планирования выпусков подкастов."""

from collections import Counter
from getpass import getpass

from models import Admin, Author, ReleaseStatus, User
from models.episodes import (
    add_episode,
    delete_episode,
    filter_by_status,
    find_episode_by_id,
    find_episodes,
    sort_by_release_date,
)
from models.podcasts import (
    add_podcast,
    find_podcast_by_id,
)
from storage import (
    load_episodes,
    load_podcasts,
    load_topics,
    load_users,
    save_episodes,
    save_podcasts,
    save_topics,
    save_users,
)
from utils import input_date, input_int, input_status, input_text

USERS_FILE = "data/users.json"
PODCASTS_FILE = "data/podcasts.json"
TOPICS_FILE = "data/topics.json"
EPISODES_FILE = "data/episodes.json"


def authenticate(users: list[User]) -> User | None:
    """Авторизовать пользователя."""
    print("\n=== Авторизация ===")
    for _ in range(3):
        login = input_text("Логин: ")
        password = getpass("Пароль: ")

        user = next(
            (item for item in users if item.login == login),
            None,
        )
        if user and user.verify_password(password):
            return user

        print("Неверный логин или пароль.")

    print("Превышено количество попыток входа.")
    return None


def show_items(items: list[object], empty_message: str) -> None:
    """Вывести объекты."""
    if not items:
        print(empty_message)
        return

    for item in items:
        print(item)
        print("-" * 70)


def show_admin_statistics(
    podcasts,
    topics,
    episodes,
) -> None:
    """Показать общую статистику компании."""
    status_counts = Counter(item.status for item in episodes)
    author_counts = Counter(item.author.name for item in episodes)
    podcast_counts = Counter(item.podcast.title for item in episodes)

    print("\n=== Общая статистика компании ===")
    print(f"Подкастов: {len(podcasts)}")
    print(f"Тем: {len(topics)}")
    print(f"Выпусков: {len(episodes)}")

    print("\nПо статусам:")
    for status in ReleaseStatus:
        count = status_counts.get(status, 0)
        percent = count / len(episodes) * 100 if episodes else 0
        print(f"- {status.title}: {count} ({percent:.1f}%)")

    print("\nТоп-5 подкастов по числу выпусков:")
    for title, count in podcast_counts.most_common(5):
        print(f"- {title}: {count}")

    print("\nТоп-5 авторов по числу выпусков:")
    for name, count in author_counts.most_common(5):
        print(f"- {name}: {count}")

    published = status_counts.get(ReleaseStatus.PUBLISHED, 0)
    percent = published / len(episodes) * 100 if episodes else 0
    print(
        f"\nОпубликовано: {published} из {len(episodes)} "
        f"({percent:.1f}%)"
    )


def show_author_statistics(
    author: Author,
    podcasts,
    episodes,
) -> None:
    """Показать статистику только по данным автора."""
    own_podcasts = [
        item for item in podcasts if item.author.id == author.id
    ]
    own_episodes = [
        item for item in episodes if item.author.id == author.id
    ]
    counts = Counter(item.status for item in own_episodes)

    print(f"\n=== Статистика автора: {author.name} ===")
    print(f"Моих подкастов: {len(own_podcasts)}")
    print(f"Моих выпусков: {len(own_episodes)}")

    print("\nПо статусам:")
    for status in ReleaseStatus:
        print(f"- {status.title}: {counts.get(status, 0)}")

    print("\nПо подкастам:")
    for podcast in sorted(own_podcasts, key=lambda item: item.id):
        count = sum(
            1
            for episode in own_episodes
            if episode.podcast.id == podcast.id
        )
        print(f"- {podcast.title}: {count} выпусков")


def choose_author(users: list[User]) -> Author | None:
    """Выбрать автора из базы сотрудников."""
    authors = [item for item in users if isinstance(item, Author)]
    show_items(authors, "Авторов нет.")
    if not authors:
        return None

    author_id = input_int("ID автора: ")
    return next(
        (item for item in authors if item.id == author_id),
        None,
    )


def add_author(users: list[User]) -> None:
    """Добавить автора в базу компании."""
    name = input_text("ФИО автора: ")
    login = input_text("Логин автора: ")
    password = input_text("Пароль автора: ")

    if any(user.login == login for user in users):
        print("Пользователь с таким логином уже существует.")
        return

    from models.users import Author, hash_password

    next_id = max((item.id for item in users), default=0) + 1
    users.append(
        Author(
            next_id,
            name,
            login,
            hash_password(password),
        )
    )
    print("Автор добавлен.")


def admin_menu(
    admin: Admin,
    users,
    podcasts,
    topics,
    episodes,
) -> None:
    """Меню администратора."""
    while True:
        print(f"\n=== Администратор: {admin.name} ===")
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
        print("12. Общая статистика")
        print("13. Показать авторов")
        print("14. Добавить автора")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_items(
                sorted(podcasts, key=lambda item: item.id),
                "Подкастов нет.",
            )

        elif choice == "2":
            author = choose_author(users)
            if author is None:
                print("Автор не найден.")
                continue
            title = input_text("Название подкаста: ")
            description = input_text("Описание: ")
            podcast = add_podcast(
                podcasts,
                title,
                description,
                author,
            )
            print(f"Добавлен подкаст #{podcast.id}.")

        elif choice == "3":
            show_items(topics, "Тем нет.")

        elif choice == "4":
            name = input_text("Название темы: ")
            if any(
                topic.name.lower() == name.lower()
                for topic in topics
            ):
                print("Такая тема уже существует.")
                continue
            from models import Topic
            next_id = max((item.id for item in topics), default=0) + 1
            topics.append(Topic(next_id, name))
            print("Тема добавлена.")

        elif choice == "5":
            show_items(
                sorted(episodes, key=lambda item: item.id),
                "Выпусков нет.",
            )

        elif choice == "6":
            podcast_id = input_int("ID подкаста: ")
            podcast = find_podcast_by_id(podcasts, podcast_id)
            if podcast is None:
                print("Подкаст не найден.")
                continue

            show_items(topics, "Тем нет.")
            topic_id = input_int("ID темы: ")
            topic = next(
                (item for item in topics if item.id == topic_id),
                None,
            )
            if topic is None:
                print("Тема не найдена.")
                continue

            author = choose_author(users)
            if author is None:
                print("Автор не найден.")
                continue

            title = input_text("Название выпуска: ")
            status = input_status("Статус: ")
            release_date = input_date("Дата (ГГГГ-ММ-ДД): ")
            episode = add_episode(
                episodes,
                podcast,
                title,
                topic,
                author,
                status,
                release_date,
            )
            print(f"Добавлен выпуск #{episode.id}.")

        elif choice == "7":
            query = input_text("Название, тема или подкаст: ")
            show_items(
                find_episodes(episodes, query),
                "Выпуски не найдены.",
            )

        elif choice == "8":
            episode_id = input_int("ID выпуска: ")
            episode = find_episode_by_id(episodes, episode_id)
            if episode is None:
                print("Выпуск не найден.")
                continue
            episode.change_status(
                input_status("Новый статус: ")
            )
            print("Статус изменен.")

        elif choice == "9":
            episode_id = input_int("ID выпуска: ")
            print(
                "Выпуск удален."
                if delete_episode(episodes, episode_id)
                else "Выпуск не найден."
            )

        elif choice == "10":
            status = input_status("Статус: ")
            show_items(
                filter_by_status(episodes, status),
                "Выпуски не найдены.",
            )

        elif choice == "11":
            show_items(
                sort_by_release_date(episodes),
                "Выпусков нет.",
            )

        elif choice == "12":
            show_admin_statistics(podcasts, topics, episodes)

        elif choice == "13":
            authors = [
                item for item in users if isinstance(item, Author)
            ]
            show_items(authors, "Авторов нет.")

        elif choice == "14":
            add_author(users)

        elif choice == "0":
            break

        else:
            print("Неизвестная команда.")


def author_menu(
    author: Author,
    podcasts,
    episodes,
) -> None:
    """Личный кабинет автора: только просмотр."""
    while True:
        print(f"\n=== Кабинет автора: {author.name} ===")
        print("1. Мои подкасты")
        print("2. Мои выпуски")
        print("3. Моя статистика")
        print("4. Опубликованные выпуски")
        print("5. Неопубликованные выпуски")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        own_podcasts = [
            item for item in podcasts if item.author.id == author.id
        ]
        own_episodes = [
            item for item in episodes if item.author.id == author.id
        ]

        if choice == "1":
            show_items(own_podcasts, "У вас нет подкастов.")

        elif choice == "2":
            show_items(own_episodes, "У вас нет выпусков.")

        elif choice == "3":
            show_author_statistics(
                author,
                podcasts,
                episodes,
            )

        elif choice == "4":
            published = [
                item for item in own_episodes if item.is_published
            ]
            show_items(
                published,
                "Опубликованных выпусков нет.",
            )

        elif choice == "5":
            not_published = [
                item for item in own_episodes
                if not item.is_published
            ]
            show_items(
                not_published,
                "Неопубликованных выпусков нет.",
            )

        elif choice == "0":
            break

        else:
            print("Неизвестная команда.")


def save_all(users, podcasts, topics, episodes) -> None:
    """Сохранить все данные."""
    save_users(USERS_FILE, users)
    save_podcasts(PODCASTS_FILE, podcasts)
    save_topics(TOPICS_FILE, topics)
    save_episodes(EPISODES_FILE, episodes)


def main() -> None:
    """Запустить приложение."""
    users = load_users(USERS_FILE)
    topics = load_topics(TOPICS_FILE)
    podcasts = load_podcasts(PODCASTS_FILE, users)
    episodes = load_episodes(
        EPISODES_FILE,
        podcasts,
        topics,
        users,
    )

    user = authenticate(users)
    if user is None:
        return

    if isinstance(user, Admin):
        admin_menu(
            user,
            users,
            podcasts,
            topics,
            episodes,
        )
    elif isinstance(user, Author):
        author_menu(user, podcasts, episodes)

    save_all(users, podcasts, topics, episodes)
    print("Данные сохранены. До свидания.")


if __name__ == "__main__":
    main()
