"""Общий контекст авторизации для Django-шаблонов."""

from authors_web.models import User

from .auth import get_current_user


def current_user_context(request):
    user = get_current_user(request)
    role = user.role if user is not None else None
    return {
        "current_user": user,
        "is_admin": role == User.Role.ADMIN,
        "is_author": role == User.Role.AUTHOR,
    }
