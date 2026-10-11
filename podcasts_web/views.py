"""Web-интерфейс подкастов."""

from html import escape

from django.http import HttpResponse
from django.shortcuts import redirect

from homepage.auth import admin_required, login_required
from homepage.views import csrf_input, not_found_response, page
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
    users = load_users(USERS_FILE)
    topics = load_topics(TOPICS_FILE)
    podcasts_list = load_podcasts(PODCASTS_FILE, users)
    episodes = load_episodes(
        EPISODES_FILE,
        podcasts_list,
        topics,
        users,
    )
    return users, podcasts_list, episodes


@login_required
def podcasts(request):
    """Список подкастов; автор видит только свои."""
    users, podcasts_list, episodes = _load_data()
    user = request.current_user

    if isinstance(user, Author):
        podcasts_list = [
            item for item in podcasts_list
            if item.author.id == user.id
        ]

    add_form = ""
    if isinstance(user, Admin):
        authors = [
            item for item in users if isinstance(item, Author)
        ]
        options = "".join(
            f'<option value="{item.id}">'
            f'{escape(item.name)}</option>'
            for item in authors
        )

        add_form = f"""
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-body">
                <h2 class="h4">Добавить подкаст</h2>
                <form method="post">
                    {csrf_input(request)}
                    <div class="row g-2">
                        <div class="col-md-4">
                            <input class="form-control"
                                   name="title"
                                   placeholder="Название"
                                   required>
                        </div>
                        <div class="col-md-4">
                            <input class="form-control"
                                   name="description"
                                   placeholder="Описание"
                                   required>
                        </div>
                        <div class="col-md-3">
                            <select class="form-select"
                                    name="author_id"
                                    required>
                                {options}
                            </select>
                        </div>
                        <div class="col-md-1">
                            <button class="btn btn-primary">
                                +
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        """

    if request.method == "POST":
        if not isinstance(user, Admin):
            from homepage.auth import forbidden_page
            return forbidden_page()

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
                item for item in users
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

        return redirect("/podcasts/")

    cards = ""
    for podcast in sorted(
        podcasts_list,
        key=lambda item: item.id,
    ):
        count = sum(
            1
            for episode in episodes
            if episode.podcast.id == podcast.id
        )

        cards += f"""
        <div class="col-md-6 col-lg-4">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body d-flex flex-column">
                    <h2 class="h5">{escape(podcast.title)}</h2>
                    <p class="text-muted">
                        {escape(podcast.description)}
                    </p>
                    <p>
                        <strong>Автор:</strong>
                        {escape(podcast.author.name)}
                    </p>
                    <span class="badge text-bg-secondary mb-3">
                        Выпусков: {count}
                    </span>
                    <a href="/podcasts/{podcast.id}/"
                       class="btn btn-primary mt-auto">
                        Подробнее
                    </a>
                </div>
            </div>
        </div>
        """

    content = f"""
    <h1>Подкасты</h1>
    <p class="text-muted">
        Автор видит только свои подкасты,
        администратор — все.
    </p>
    {add_form}
    <div class="row g-3">{cards}</div>
    """

    return HttpResponse(page("Подкасты", content, request))


@login_required
def podcast_detail(request, podcast_id):
    """Карточка подкаста."""
    _, podcasts_list, episodes = _load_data()
    user = request.current_user
    podcast = find_podcast_by_id(
        podcasts_list,
        podcast_id,
    )

    if podcast is None:
        return not_found_response(
            request,
            f"Подкаст #{podcast_id} не найден.",
        )

    if (
        isinstance(user, Author)
        and podcast.author.id != user.id
    ):
        from homepage.auth import forbidden_page
        return forbidden_page()

    podcast_episodes = [
        item for item in episodes
        if item.podcast.id == podcast.id
    ]

    items = "".join(
        f"""
        <a href="/episodes/{item.id}/"
           class="list-group-item list-group-item-action">
            <div class="d-flex justify-content-between">
                <strong>{escape(item.title)}</strong>
                <span>{escape(item.release_date)}</span>
            </div>
            <small>{escape(item.status.title)}</small>
        </a>
        """
        for item in sorted(
            podcast_episodes,
            key=lambda item: item.release_date,
        )
    )

    content = f"""
    <a href="/podcasts/"
       class="btn btn-sm btn-outline-secondary mb-3">
        ← Все подкасты
    </a>

    <div class="card shadow-sm border-0 mb-4">
        <div class="card-body">
            <h1>{escape(podcast.title)}</h1>
            <p class="lead">
                {escape(podcast.description)}
            </p>
            <p><strong>ID:</strong> {podcast.id}</p>
            <p>
                <strong>Автор:</strong>
                {escape(podcast.author.name)}
            </p>
            <p class="mb-0">
                <strong>Выпусков:</strong>
                {len(podcast_episodes)}
            </p>
        </div>
    </div>

    <h2 class="h4">Выпуски подкаста</h2>
    <div class="list-group">
        {items or '<div class="alert alert-info">Выпусков нет.</div>'}
    </div>
    """

    return HttpResponse(page(podcast.title, content, request))
