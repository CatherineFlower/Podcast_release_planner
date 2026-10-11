"""Web-интерфейс выпусков."""

from html import escape

from django.http import HttpResponse
from django.shortcuts import redirect

from homepage.auth import login_required
from homepage.views import csrf_input, not_found_response, page
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


def _badge(status):
    classes = {
        ReleaseStatus.IDEA: "text-bg-secondary",
        ReleaseStatus.PLANNED: "text-bg-primary",
        ReleaseStatus.RECORDING: "text-bg-warning",
        ReleaseStatus.READY: "text-bg-info",
        ReleaseStatus.PUBLISHED: "text-bg-success",
    }
    return classes.get(status, "text-bg-secondary")


@login_required
def episodes(request):
    """Список, поиск, фильтр, сортировка и добавление выпуска."""
    users, topics, podcasts, episodes_list = _load_data()
    user = request.current_user

    if isinstance(user, Author):
        episodes_list = [
            item for item in episodes_list
            if item.author.id == user.id
        ]

    if request.method == "POST":
        if not isinstance(user, Admin):
            from homepage.auth import forbidden_page
            return forbidden_page()

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
            return redirect("/episodes/")

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
                item for item in users
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

        if all(
            [
                podcast is not None,
                topic is not None,
                author is not None,
                title,
                release_date,
                status is not None,
            ]
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

        return redirect("/episodes/")

    query = request.GET.get("q", "").strip()
    status_value = request.GET.get("status", "").strip()
    sort_value = request.GET.get("sort", "").strip()

    if query:
        episodes_list = find_episodes(
            episodes_list,
            query,
        )

    if status_value:
        try:
            status = ReleaseStatus.from_value(status_value)
            episodes_list = filter_by_status(
                episodes_list,
                status,
            )
        except ValueError:
            pass

    if sort_value == "date":
        episodes_list = sort_by_release_date(
            episodes_list
        )

    form = ""
    if isinstance(user, Admin):
        podcast_options = "".join(
            f'<option value="{item.id}">'
            f'{escape(item.title)}</option>'
            for item in podcasts
        )
        topic_options = "".join(
            f'<option value="{item.id}">'
            f'{escape(item.name)}</option>'
            for item in topics
        )
        author_options = "".join(
            f'<option value="{item.id}">'
            f'{escape(item.name)}</option>'
            for item in users
            if isinstance(item, Author)
        )
        status_options = "".join(
            f'<option value="{item.value}">'
            f'{escape(item.title)}</option>'
            for item in ReleaseStatus
        )

        form = f"""
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-body">
                <h2 class="h4">Добавить выпуск</h2>
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
                            <select class="form-select"
                                    name="podcast_id">
                                {podcast_options}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <select class="form-select"
                                    name="topic_id">
                                {topic_options}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <select class="form-select"
                                    name="author_id">
                                {author_options}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <select class="form-select"
                                    name="status">
                                {status_options}
                            </select>
                        </div>
                        <div class="col-md-4">
                            <input class="form-control"
                                   type="date"
                                   name="release_date"
                                   required>
                        </div>
                    </div>
                    <button class="btn btn-primary mt-3">
                        Добавить
                    </button>
                </form>
            </div>
        </div>
        """

    status_filter = "".join(
        f'<option value="{item.value}">'
        f'{escape(item.title)}</option>'
        for item in ReleaseStatus
    )

    rows = ""
    for item in episodes_list:
        rows += f"""
        <tr>
            <td>
                <a href="/episodes/{item.id}/">
                    {escape(item.title)}
                </a>
            </td>
            <td>{escape(item.podcast.title)}</td>
            <td>{escape(item.author.name)}</td>
            <td>{escape(item.release_date)}</td>
            <td>
                <span class="badge {_badge(item.status)}">
                    {escape(item.status.title)}
                </span>
            </td>
        </tr>
        """

    content = f"""
    <h1>Выпуски</h1>

    {form}

    <div class="card shadow-sm border-0 mb-4">
        <div class="card-body">
            <form method="get" class="row g-2">
                <div class="col-md-5">
                    <input class="form-control"
                           name="q"
                           value="{escape(query)}"
                           placeholder="Название, тема или подкаст">
                </div>
                <div class="col-md-3">
                    <select class="form-select" name="status">
                        <option value="">Все статусы</option>
                        {status_filter}
                    </select>
                </div>
                <div class="col-md-2">
                    <select class="form-select" name="sort">
                        <option value="">Без сортировки</option>
                        <option value="date">
                            По дате
                        </option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-secondary w-100">
                        Применить
                    </button>
                </div>
            </form>
        </div>
    </div>

    <div class="card table-card shadow-sm">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-dark">
                    <tr>
                        <th>Выпуск</th>
                        <th>Подкаст</th>
                        <th>Автор</th>
                        <th>Дата</th>
                        <th>Статус</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </div>
    """

    return HttpResponse(page("Выпуски", content, request))


@login_required
def episode_detail(request, episode_id):
    """Карточка, изменение статуса и удаление выпуска."""
    _, _, _, all_episodes = _load_data()
    user = request.current_user
    episode = find_episode_by_id(
        all_episodes,
        episode_id,
    )

    if episode is None:
        return not_found_response(
            request,
            f"Выпуск #{episode_id} не найден.",
        )

    if (
        isinstance(user, Author)
        and episode.author.id != user.id
    ):
        from homepage.auth import forbidden_page
        return forbidden_page()

    if request.method == "POST":
        if not isinstance(user, Admin):
            from homepage.auth import forbidden_page
            return forbidden_page()

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
            return redirect("/episodes/")

        return redirect(f"/episodes/{episode.id}/")

    controls = ""
    if isinstance(user, Admin):
        options = "".join(
            f'<option value="{status.value}">'
            f'{escape(status.title)}</option>'
            for status in ReleaseStatus
        )
        controls = f"""
        <div class="card shadow-sm border-0 mt-4">
            <div class="card-body">
                <h2 class="h5">Управление выпуском</h2>

                <form method="post" class="mb-3">
                    {csrf_input(request)}
                    <input type="hidden"
                           name="action"
                           value="status">
                    <div class="input-group">
                        <select class="form-select"
                                name="status">
                            {options}
                        </select>
                        <button class="btn btn-primary">
                            Изменить статус
                        </button>
                    </div>
                </form>

                <form method="post">
                    {csrf_input(request)}
                    <input type="hidden"
                           name="action"
                           value="delete">
                    <button class="btn btn-danger">
                        Удалить выпуск
                    </button>
                </form>
            </div>
        </div>
        """

    content = f"""
    <a href="/episodes/"
       class="btn btn-sm btn-outline-secondary mb-3">
        ← Все выпуски
    </a>

    <div class="card shadow-sm border-0">
        <div class="card-body">
            <h1 class="h3">{escape(episode.title)}</h1>
            <p>
                <strong>Подкаст:</strong>
                {escape(episode.podcast.title)}
            </p>
            <p>
                <strong>Автор:</strong>
                {escape(episode.author.name)}
            </p>
            <p>
                <strong>Тема:</strong>
                {escape(episode.topic.name)}
            </p>
            <p>
                <strong>Дата:</strong>
                {escape(episode.release_date)}
            </p>
            <span class="badge {_badge(episode.status)}">
                {escape(episode.status.title)}
            </span>
        </div>
    </div>

    {controls}
    """

    return HttpResponse(page(episode.title, content, request))
