"""View-функции страниц подкастов."""

from django.shortcuts import redirect, render

from homepage.auth import (
    forbidden_response,
    login_required,
)
from models import Admin, Author
from models.podcasts import (
    add_podcast,
    find_podcast_by_id,
)
from storage import (
    load_episodes,
    load_podcasts,
    load_topics,
    load_users,
    save_podcasts,
)

USERS_FILE = "data/users.json"
PODCASTS_FILE = "data/podcasts.json"
TOPICS_FILE = "data/topics.json"
EPISODES_FILE = "data/episodes.json"


def _load_data():
    """Загрузить пользователей, подкасты и выпуски."""
    users = load_users(USERS_FILE)
    topics = load_topics(TOPICS_FILE)
    podcasts = load_podcasts(PODCASTS_FILE, users)
    episodes = load_episodes(
        EPISODES_FILE,
        podcasts,
        topics,
        users,
    )
    return users, podcasts, episodes


@login_required
def podcasts(request):
    """Список подкастов и добавление подкаста администратором."""
    users, podcasts_list, episodes = _load_data()
    user = request.current_user

    if isinstance(user, Author):
        podcasts_list = [
            item
            for item in podcasts_list
            if item.author.id == user.id
        ]

    if request.method == "POST":
        if not isinstance(user, Admin):
            return forbidden_response(request)

        title = request.POST.get("title", "").strip()
        description = request.POST.get(
            "description",
            "",
        ).strip()

        try:
            author_id = int(
                request.POST.get("author_id", "0")
            )
        except ValueError:
            author_id = 0

        author = next(
            (
                item
                for item in users
                if isinstance(item, Author)
                and item.id == author_id
            ),
            None,
        )

        if title and description and author is not None:
            add_podcast(
                podcasts_list,
                title,
                description,
                author,
            )
            save_podcasts(
                PODCASTS_FILE,
                podcasts_list,
            )

        return redirect("podcasts_web:podcasts")

    episode_counts = {}
    for podcast in podcasts_list:
        episode_counts[podcast.id] = sum(
            1
            for episode in episodes
            if episode.podcast.id == podcast.id
        )

    context = {
        "podcasts": podcasts_list,
        "authors": [
            item
            for item in users
            if isinstance(item, Author)
        ],
        "episode_counts": episode_counts,
    }

    return render(
        request,
        "podcasts_web/podcast_list.html",
        context,
    )


@login_required
def podcast_detail(request, podcast_id):
    """Страница отдельного подкаста."""
    _, podcasts_list, episodes = _load_data()
    user = request.current_user

    podcast = find_podcast_by_id(
        podcasts_list,
        podcast_id,
    )

    if (
        podcast is not None
        and isinstance(user, Author)
        and podcast.author.id != user.id
    ):
        return forbidden_response(request)

    podcast_episodes = []
    if podcast is not None:
        podcast_episodes = [
            episode
            for episode in episodes
            if episode.podcast.id == podcast.id
        ]

    context = {
        "podcast": podcast,
        "podcast_episodes": podcast_episodes,
    }

    return render(
        request,
        "podcasts_web/podcast_detail.html",
        context,
        status=404 if podcast is None else 200,
    )
