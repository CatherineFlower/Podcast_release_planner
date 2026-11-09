"""Главная, авторизация и статистика на Django ORM (ПР9)."""

from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from authors_web.models import User
from episodes_web.models import Episode
from podcasts_web.models import Podcast
from topics_web.models import Topic

from .auth import SESSION_USER_ID, get_current_user, login_required


def login_view(request):
    current = get_current_user(request)
    if current is not None:
        return redirect("homepage:index")

    error = None
    if request.method == "POST":
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")
        user = User.objects.filter(login=login).first()
        if user is not None and user.verify_password(password):
            request.session[SESSION_USER_ID] = user.pk
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect("homepage:index")
        error = "Неверный логин или пароль."

    return render(request, "homepage/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("homepage:login")


def _episode_scope(user):
    queryset = Episode.objects.all()
    if user.role == User.Role.AUTHOR:
        queryset = queryset.filter(author=user)
    return queryset


def _podcast_scope(user):
    queryset = Podcast.objects.all()
    if user.role == User.Role.AUTHOR:
        queryset = queryset.filter(author=user)
    return queryset


@login_required
def index(request):
    user = request.current_user
    episodes = _episode_scope(user)
    podcasts = _podcast_scope(user)

    totals = episodes.aggregate(
        episode_count=Count("id"),
        published_count=Count(
            "id",
            filter=Q(status=Episode.Status.PUBLISHED),
        ),
    )
    dashboard = {
        "podcast_count": podcasts.count(),
        "episode_count": totals["episode_count"],
        "published_count": totals["published_count"],
        "in_progress_count": episodes.in_progress().count(),
        "topic_count": Topic.objects.count(),
        "author_count": User.objects.filter(
            role=User.Role.AUTHOR
        ).count(),
    }

    upcoming = (
        episodes.in_progress().select_related("podcast", "author")
        .order_by("release_date", "pk")[:5]
    )

    return render(
        request,
        "homepage/index.html",
        {"dashboard": dashboard, "upcoming_episodes": upcoming},
    )


@login_required
def statistics(request):
    user = request.current_user
    episodes = _episode_scope(user)
    podcasts = _podcast_scope(user)

    totals = episodes.aggregate(
        episode_count=Count("id"),
        published_count=Count(
            "id",
            filter=Q(status=Episode.Status.PUBLISHED),
        ),
    )
    dashboard = {
        "podcast_count": podcasts.count(),
        **totals,
    }

    grouped = {
        row["status"]: row["count"]
        for row in (
            episodes.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
    }
    status_rows = []
    total = totals["episode_count"] or 0
    for value, title in Episode.Status.choices:
        count = grouped.get(value, 0)
        status_rows.append(
            {
                "title": title,
                "count": count,
                "percent": f"{(count / total * 100) if total else 0:.1f}",
            }
        )

    podcast_rows = (
        podcasts.annotate(
            episodes_count=Count("episodes"),
            published_count=Count(
                "episodes",
                filter=Q(episodes__status=Episode.Status.PUBLISHED),
            ),
        )
        .values("id", "title", "episodes_count", "published_count")
        .order_by("-episodes_count", "title")
    )

    return render(
        request,
        "homepage/statistics.html",
        {
            "dashboard": dashboard,
            "status_rows": status_rows,
            "podcast_rows": podcast_rows,
            "personal": user.role == User.Role.AUTHOR,
        },
    )


def page_not_found(request, exception):
    return render(
        request,
        "errors/404.html",
        {"requested_path": request.get_full_path()},
        status=404,
    )


def catch_all_404(request, path=None):
    return render(
        request,
        "errors/404.html",
        {"requested_path": request.get_full_path()},
        status=404,
    )
