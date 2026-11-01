"""Общий контекст авторизации для Django-шаблонов."""

from .auth import get_current_user


def current_user_context(request):
    user = get_current_user(request)
    role = user["role"] if user is not None else None
    return {
        "current_user": user,
        "is_admin": role == "admin",
        "is_author": role == "author",
    }
