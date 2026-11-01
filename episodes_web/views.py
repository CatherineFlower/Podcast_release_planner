"""View-функции страниц выпусков."""

from django.shortcuts import redirect, render

from homepage.auth import (
    forbidden_response,
    login_required,
)
from models import Admin, Author, ReleaseStatus
from models.episodes import (
    add_episode,
    delete_episode,
    filter_by_status,
    find_episode_by_id,
    find_episodes,
    sort_by_release_date,
)
from models.podcasts import find_podcast_by_id
from storage import (
    load_episodes,
    load_podcasts,
    load_topics,
    load_users,
    save_episodes,
)

USERS_FILE = "data/users.json"
PODCASTS_FILE = "data/podcasts.json"
TOPICS_FILE = "data/topics.json"
EPISODES_FILE = "data/episodes.json"


def _load_data():
    """Загрузить данные выпусков."""
    users = load_users(USERS_FILE)
    topics = load_topics(TOPICS_FILE)
    podcasts = load_podcasts(PODCASTS_FILE, users)
    episodes = load_episodes(
        EPISODES_FILE,
        podcasts,
        topics,
        users,
    )
    return users, topics, podcasts, episodes


@login_required
def episodes(request):
    """Список, поиск, фильтрация, сортировка и добавление."""
    users, topics, podcasts, episodes_list = _load_data()
    user = request.current_user

    if isinstance(user, Author):
        episodes_list = [
            item
            for item in episodes_list
            if item.author.id == user.id
        ]

    if request.method == "POST":
        if not isinstance(user, Admin):
            return forbidden_response(request)

        try:
            podcast_id = int(
                request.POST.get("podcast_id", "0")
            )
            topic_id = int(
                request.POST.get("topic_id", "0")
            )
            author_id = int(
                request.POST.get("author_id", "0")
            )
        except ValueError:
            return redirect("episodes_web:episodes")

        podcast = find_podcast_by_id(
            podcasts,
            podcast_id,
        )
        topic = next(
            (item for item in topics if item.id == topic_id),
            None,
        )
        author = next(
            (
                item
                for item in users
                if isinstance(item, Author)
                and item.id == author_id
            ),
            None,
        )

        title = request.POST.get("title", "").strip()
        release_date = request.POST.get(
            "release_date",
            "",
        ).strip()

        try:
            status = ReleaseStatus.from_value(
                request.POST.get("status", "")
            )
        except ValueError:
            status = None

        if (
            podcast is not None
            and topic is not None
            and author is not None
            and title
            and release_date
            and status is not None
        ):
            all_episodes = _load_data()[3]
            add_episode(
                all_episodes,
                podcast,
                title,
                topic,
                author,
                status,
                release_date,
            )
            save_episodes(
                EPISODES_FILE,
                all_episodes,
            )

        return redirect("episodes_web:episodes")

    query = request.GET.get("q", "").strip()
    status_value = request.GET.get(
        "status",
        "",
    ).strip()
    sort_value = request.GET.get(
        "sort",
        "",
    ).strip()

    if query:
        episodes_list = find_episodes(
            episodes_list,
            query,
        )

    if status_value:
        try:
            filter_status = ReleaseStatus.from_value(
                status_value
            )
            episodes_list = filter_by_status(
                episodes_list,
                filter_status,
            )
        except ValueError:
            pass

    if sort_value == "date":
        episodes_list = sort_by_release_date(
            episodes_list
        )

    context = {
        "episodes": episodes_list,
        "podcasts": podcasts,
        "topics": topics,
        "authors": [
            item
            for item in users
            if isinstance(item, Author)
        ],
        "statuses": list(ReleaseStatus),
        "query": query,
        "selected_status": status_value,
        "selected_sort": sort_value,
    }

    return render(
        request,
        "episodes_web/episode_list.html",
        context,
    )


@login_required
def episode_detail(request, episode_id):
    """Страница выпуска, изменение статуса и удаление."""
    _, _, _, all_episodes = _load_data()
    user = request.current_user

    episode = find_episode_by_id(
        all_episodes,
        episode_id,
    )

    if (
        episode is not None
        and isinstance(user, Author)
        and episode.author.id != user.id
    ):
        return forbidden_response(request)

    if episode is not None and request.method == "POST":
        if not isinstance(user, Admin):
            return forbidden_response(request)

        action = request.POST.get("action", "")

        if action == "status":
            try:
                new_status = ReleaseStatus.from_value(
                    request.POST.get("status", "")
                )
                episode.change_status(new_status)
                save_episodes(
                    EPISODES_FILE,
                    all_episodes,
                )
            except ValueError:
                pass

        elif action == "delete":
            delete_episode(
                all_episodes,
                episode.id,
            )
            save_episodes(
                EPISODES_FILE,
                all_episodes,
            )
            return redirect("episodes_web:episodes")

        return redirect(
            "episodes_web:detail",
            episode_id=episode.id,
        )

    context = {
        "episode": episode,
        "statuses": list(ReleaseStatus),
    }

    return render(
        request,
        "episodes_web/episode_detail.html",
        context,
        status=404 if episode is None else 200,
    )
