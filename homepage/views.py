"""Главная, авторизация и SQL-статистика ПР7."""

from django.conf import settings
from django.shortcuts import redirect, render

from db.repository import (
    get_dashboard,
    get_podcast_statistics,
    get_status_statistics,
    get_user_by_login,
)
from models.users import hash_password

from .auth import SESSION_USER_ID, get_current_user, login_required


def login_view(request):
    current = get_current_user(request)
    if current is not None:
        return redirect("homepage:index")

    error = None
    if request.method == "POST":
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")
        user = get_user_by_login(login)
        if (
            user is not None
            and user["password_hash"] == hash_password(password)
        ):
            request.session[SESSION_USER_ID] = user["id"]
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect("homepage:index")
        error = "Неверный логин или пароль."

    return render(request, "homepage/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("homepage:login")


@login_required
def index(request):
    user = request.current_user
    author_id = user["id"] if user["role"] == "author" else None
    dashboard = get_dashboard(author_id)
    return render(
        request,
        "homepage/index.html",
        {"dashboard": dashboard},
    )


@login_required
def statistics(request):
    user = request.current_user
    author_id = user["id"] if user["role"] == "author" else None
    dashboard = get_dashboard(author_id)
    return render(
        request,
        "homepage/statistics.html",
        {
            "dashboard": dashboard,
            "status_rows": get_status_statistics(author_id),
            "podcast_rows": get_podcast_statistics(author_id),
            "personal": author_id is not None,
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
