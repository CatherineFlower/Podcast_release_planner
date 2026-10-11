"""Авторизация веб-интерфейса через данные ПР3 и Django-сессии."""

from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect

from models import Admin, Author
from storage import load_users

USERS_FILE = "data/users.json"
SESSION_USER_ID = "podcast_planner_user_id"


def get_current_user(request):
    """Вернуть вошедшего пользователя по ID из сессии."""
    user_id = request.session.get(SESSION_USER_ID)
    if user_id is None:
        return None

    users = load_users(USERS_FILE)
    return next(
        (user for user in users if user.id == user_id),
        None,
    )


def login_required(view_func):
    """Разрешить view только авторизованному пользователю."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("/login/")
        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    """Разрешить view только администратору."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("/login/")
        if not isinstance(user, Admin):
            return forbidden_page()
        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def author_required(view_func):
    """Разрешить view автору или администратору."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("/login/")
        if not isinstance(user, (Admin, Author)):
            return forbidden_page()
        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def forbidden_page():
    """Красивый HTTP 403."""
    from homepage.views import page

    content = """
    <div class="text-center py-5">
        <div class="display-1 text-danger fw-bold">403</div>
        <h1>Доступ запрещён</h1>
        <p class="text-muted">
            У вашей роли нет прав на эту операцию.
        </p>
        <a href="/" class="btn btn-primary">
            На главную
        </a>
    </div>
    """
    return HttpResponse(
        page("403 — доступ запрещён", content),
        status=403,
    )
