"""Главные страницы проекта ПР6 на Django Templates."""

from collections import Counter

from django.conf import settings
from django.shortcuts import redirect, render

from models import Author, ReleaseStatus
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


def _load_all():
    """Загрузить объекты предметной области из JSON."""
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
    """Авторизовать пользователя и сохранить его сессию."""
    current = get_current_user(request)
    if current is not None:
        return redirect("homepage:index")

    error = None

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
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect("homepage:index")

        error = "Неверный логин или пароль."

    return render(
        request,
        "homepage/login.html",
        {"error": error},
    )


def logout_view(request):
    """Завершить сессию пользователя."""
    request.session.flush()
    return redirect("homepage:login")


@login_required
def index(request):
    """Главная страница после авторизации."""
    users, topics, podcasts, episodes = _load_all()
    user = request.current_user

    if isinstance(user, Author):
        podcasts = [
            item
            for item in podcasts
            if item.author.id == user.id
        ]
        episodes = [
            item
            for item in episodes
            if item.author.id == user.id
        ]

    context = {
        "podcasts": podcasts,
        "episodes": episodes,
        "topics": topics,
        "authors_count": sum(
            1
            for item in users
            if isinstance(item, Author)
        ),
        "published_count": sum(
            1
            for item in episodes
            if item.status == ReleaseStatus.PUBLISHED
        ),
        "user": user,
    }

    return render(
        request,
        "homepage/index.html",
        context,
    )


@login_required
def statistics(request):
    """Показать общую или персональную статистику."""
    _, _, podcasts, episodes = _load_all()
    user = request.current_user

    if isinstance(user, Author):
        podcasts = [
            item
            for item in podcasts
            if item.author.id == user.id
        ]
        episodes = [
            item
            for item in episodes
            if item.author.id == user.id
        ]

    status_counts = Counter(item.status for item in episodes)
    podcast_counts = Counter(
        item.podcast.title
        for item in episodes
    )

    status_rows = []
    for status in ReleaseStatus:
        count = status_counts.get(status, 0)
        percent = (
            count / len(episodes) * 100
            if episodes
            else 0
        )
        status_rows.append(
            {
                "title": status.title,
                "count": count,
                "percent": f"{percent:.1f}",
            }
        )

    context = {
        "podcasts": podcasts,
        "episodes": episodes,
        "status_rows": status_rows,
        "podcast_rows": podcast_counts.most_common(),
        "personal": isinstance(user, Author),
    }

    return render(
        request,
        "homepage/statistics.html",
        context,
    )


def page_not_found(request, exception):
    """Стандартный обработчик Django 404."""
    return render(
        request,
        "errors/404.html",
        {"requested_path": request.get_full_path()},
        status=404,
    )


def catch_all_404(request, path=None):
    """Перехватить любой неизвестный URL красивым шаблоном."""
    return render(
        request,
        "errors/404.html",
        {"requested_path": request.get_full_path()},
        status=404,
    )
