"""Авторизация и разграничение доступа через Django-сессии."""

from functools import wraps

from django.shortcuts import redirect, render

from models import Admin, Author
from storage import load_users

USERS_FILE = "data/users.json"
SESSION_USER_ID = "podcast_planner_user_id"


def get_current_user(request):
    """Вернуть вошедшего пользователя по ID из сессии."""
    if request is None:
        return None

    user_id = request.session.get(SESSION_USER_ID)
    if user_id is None:
        return None

    users = load_users(USERS_FILE)
    return next(
        (user for user in users if user.id == user_id),
        None,
    )


def forbidden_response(request):
    """Вернуть шаблонную страницу HTTP 403."""
    return render(
        request,
        "errors/403.html",
        status=403,
    )


def login_required(view_func):
    """Разрешить view только авторизованному пользователю."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("homepage:login")

        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    """Разрешить view только администратору."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("homepage:login")

        if not isinstance(user, Admin):
            return forbidden_response(request)

        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper


def author_required(view_func):
    """Разрешить view автору или администратору."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("homepage:login")

        if not isinstance(user, (Admin, Author)):
            return forbidden_response(request)

        request.current_user = user
        return view_func(request, *args, **kwargs)

    return wrapper
