"""Главная страница, авторизация, статистика и общий HTML-каркас."""

from collections import Counter
from html import escape

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect

from models import Admin, Author, ReleaseStatus
from storage import (
    load_episodes,
    load_podcasts,
    load_topics,
    load_users,
)

from .auth import (
    SESSION_USER_ID,
    get_current_user,
    login_required,
)

USERS_FILE = "data/users.json"
PODCASTS_FILE = "data/podcasts.json"
TOPICS_FILE = "data/topics.json"
EPISODES_FILE = "data/episodes.json"


def csrf_input(request) -> str:
    """HTML-поле CSRF для ручных POST-форм."""
    token = get_token(request)
    return (
        '<input type="hidden" name="csrfmiddlewaretoken" '
        f'value="{escape(token)}">'
    )


def page(title: str, content: str, request=None) -> str:
    """Сформировать общий HTML-каркас страницы."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )

    user = get_current_user(request) if request is not None else None
    auth_block = ""

    if user is not None:
        auth_block = f"""
        <div class="d-flex align-items-center gap-2 ms-auto">
            <span class="navbar-text text-light">
                {escape(user.name)} · {escape(user.role)}
            </span>
            <a class="btn btn-sm btn-outline-light"
               href="/logout/">
                Выйти
            </a>
        </div>
        """

    nav_links = """
    <a class="nav-link" href="/">Главная</a>
    <a class="nav-link" href="/podcasts/">Подкасты</a>
    <a class="nav-link" href="/episodes/">Выпуски</a>
    <a class="nav-link" href="/statistics/">Статистика</a>
    """

    if isinstance(user, Admin):
        nav_links += """
        <a class="nav-link" href="/topics/">Темы</a>
        <a class="nav-link" href="/authors/">Авторы</a>
        """

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        body {{
            min-height: 100vh;
            background:
                linear-gradient(180deg, #f8f9fa 0%, #eef2f7 100%);
        }}
        .hero {{
            background:
                linear-gradient(135deg, #111827 0%, #374151 100%);
            color: white;
            border-radius: 1.25rem;
        }}
        .metric-card {{
            border: 0;
            border-radius: 1rem;
        }}
        .table-card {{
            border: 0;
            border-radius: 1rem;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand fw-semibold" href="/">
                Podcast Planner
            </a>
            <div class="navbar-nav">
                {nav_links}
            </div>
            {auth_block}
        </div>
    </nav>

    <main class="container pb-5">
        {content}
    </main>
</body>
</html>"""


def _load_all():
    """Загрузить объекты предметной области ПР3."""
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


def login_view(request):
    """Вход; состояние сохраняется в Django-сессии до выхода."""
    current = get_current_user(request)
    if current is not None:
        return redirect("/")

    error = ""

    if request.method == "POST":
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")
        users = load_users(USERS_FILE)

        user = next(
            (item for item in users if item.login == login),
            None,
        )

        if user is not None and user.verify_password(password):
            request.session[SESSION_USER_ID] = user.id
            request.session.set_expiry(0)
            return redirect("/")

        error = """
        <div class="alert alert-danger">
            Неверный логин или пароль.
        </div>
        """

    content = f"""
    <div class="row justify-content-center py-5">
        <div class="col-md-6 col-lg-4">
            <div class="card shadow border-0">
                <div class="card-body p-4">
                    <h1 class="h3 mb-3">Вход в систему</h1>
                    <p class="text-muted">
                        Сессия сохраняется до нажатия «Выйти».
                    </p>
                    {error}
                    <form method="post">
                        {csrf_input(request)}
                        <div class="mb-3">
                            <label class="form-label">Логин</label>
                            <input class="form-control"
                                   name="login"
                                   required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Пароль</label>
                            <input class="form-control"
                                   type="password"
                                   name="password"
                                   required>
                        </div>
                        <button class="btn btn-primary w-100">
                            Войти
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """
    return HttpResponse(page("Вход", content, request))


def logout_view(request):
    """Завершить текущую сессию пользователя."""
    request.session.flush()
    return redirect("/login/")


@login_required
def index(request):
    """Главная страница после авторизации."""
    users, topics, podcasts, episodes = _load_all()
    user = request.current_user

    if isinstance(user, Author):
        podcasts = [
            item for item in podcasts
            if item.author.id == user.id
        ]
        episodes = [
            item for item in episodes
            if item.author.id == user.id
        ]

    authors_count = sum(
        1 for item in users if isinstance(item, Author)
    )
    published = sum(
        1
        for item in episodes
        if item.status == ReleaseStatus.PUBLISHED
    )

    admin_actions = ""
    if isinstance(user, Admin):
        admin_actions = """
        <a href="/topics/" class="btn btn-outline-light me-2">
            Темы
        </a>
        <a href="/authors/" class="btn btn-outline-light">
            Авторы
        </a>
        """

    content = f"""
    <section class="hero p-5 shadow-sm mb-4">
        <h1 class="display-5 fw-bold">
            Система планирования выпусков подкастов
        </h1>
        <p class="lead">
            Роль: {escape(user.role)}.
            Данные и права взяты из проекта ПР3.
        </p>
        <a href="/podcasts/" class="btn btn-light me-2">
            Подкасты
        </a>
        <a href="/episodes/"
           class="btn btn-outline-light me-2">
            Выпуски
        </a>
        <a href="/statistics/"
           class="btn btn-outline-light me-2">
            Статистика
        </a>
        {admin_actions}
    </section>

    <div class="row g-3">
        <div class="col-md-4">
            <div class="card metric-card shadow-sm">
                <div class="card-body">
                    <div class="text-muted">Подкасты</div>
                    <div class="display-6">{len(podcasts)}</div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card metric-card shadow-sm">
                <div class="card-body">
                    <div class="text-muted">Выпуски</div>
                    <div class="display-6">{len(episodes)}</div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card metric-card shadow-sm">
                <div class="card-body">
                    <div class="text-muted">Опубликовано</div>
                    <div class="display-6">{published}</div>
                </div>
            </div>
        </div>
    </div>
    """

    if isinstance(user, Admin):
        content += f"""
        <div class="alert alert-secondary mt-4">
            В базе компании авторов: {authors_count},
            тем: {len(topics)}.
        </div>
        """

    return HttpResponse(page("Podcast Planner", content, request))


@login_required
def statistics(request):
    """Общая статистика админу и персональная автору."""
    _, _, podcasts, episodes = _load_all()
    user = request.current_user

    if isinstance(user, Author):
        podcasts = [
            item for item in podcasts
            if item.author.id == user.id
        ]
        episodes = [
            item for item in episodes
            if item.author.id == user.id
        ]

    status_counts = Counter(item.status for item in episodes)
    podcast_counts = Counter(
        item.podcast.title for item in episodes
    )

    rows = ""
    for status in ReleaseStatus:
        count = status_counts.get(status, 0)
        percent = (
            count / len(episodes) * 100
            if episodes
            else 0
        )
        rows += f"""
        <tr>
            <td>{escape(status.title)}</td>
            <td>{count}</td>
            <td>{percent:.1f}%</td>
        </tr>
        """

    podcast_rows = ""
    for title, count in podcast_counts.most_common():
        podcast_rows += f"""
        <tr>
            <td>{escape(title)}</td>
            <td>{count}</td>
        </tr>
        """

    scope = (
        "Моя статистика"
        if isinstance(user, Author)
        else "Общая статистика компании"
    )

    content = f"""
    <h1>{scope}</h1>

    <div class="row g-3 mb-4">
        <div class="col-md-6">
            <div class="card metric-card shadow-sm">
                <div class="card-body">
                    <div class="text-muted">Подкастов</div>
                    <div class="display-6">{len(podcasts)}</div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card metric-card shadow-sm">
                <div class="card-body">
                    <div class="text-muted">Выпусков</div>
                    <div class="display-6">{len(episodes)}</div>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <div class="col-lg-6">
            <div class="card table-card shadow-sm">
                <div class="card-body">
                    <h2 class="h4">По статусам</h2>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Статус</th>
                                <th>Количество</th>
                                <th>Доля</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card table-card shadow-sm">
                <div class="card-body">
                    <h2 class="h4">По подкастам</h2>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Подкаст</th>
                                <th>Выпусков</th>
                            </tr>
                        </thead>
                        <tbody>{podcast_rows}</tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    """

    return HttpResponse(page(scope, content, request))



def not_found_response(request, message: str | None = None):
    """Вернуть единую красивую страницу 404 для любого случая."""
    detail = (
        escape(message)
        if message
        else "Запрошенная страница или объект не найдены."
    )

    content = f"""
    <div class="row justify-content-center py-5">
        <div class="col-lg-7">
            <div class="card shadow border-0 text-center">
                <div class="card-body p-5">
                    <div class="display-1 fw-bold text-danger">
                        404
                    </div>
                    <h1 class="h2 mb-3">
                        Страница не найдена
                    </h1>
                    <p class="text-muted mb-4">
                        {detail}
                    </p>

                    <div class="d-flex gap-2 justify-content-center">
                        <a href="/"
                           class="btn btn-primary">
                            ← На главную
                        </a>
                        <button type="button"
                                class="btn btn-outline-secondary"
                                onclick="history.back()">
                            Назад
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    return HttpResponse(
        page("404 — страница не найдена", content, request),
        status=404,
    )


def page_not_found(request, exception):
    """Стандартный Django handler404."""
    return not_found_response(request)


def catch_all_404(request, path=None):
    """Перехватить любой URL, не совпавший с маршрутами проекта."""
    requested = request.get_full_path()
    return not_found_response(
        request,
        f"Адрес {requested} не существует.",
    )
