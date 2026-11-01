"""Общий контекст для всех Django-шаблонов."""

from models import Admin, Author

from .auth import get_current_user


def current_user_context(request):
    """Добавить текущего пользователя и его роль в контекст."""
    user = get_current_user(request)

    return {
        "current_user": user,
        "is_admin": isinstance(user, Admin),
        "is_author": isinstance(user, Author),
    }
