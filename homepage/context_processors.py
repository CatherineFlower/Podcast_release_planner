"""Общий контекст авторизации и общих данных ПР10."""

from authors_web.models import User
from episodes_web.models import Episode
from podcasts_web.models import Podcast

from .auth import get_current_user


def current_user_context(request):
    user = get_current_user(request)
    role = user.role if user is not None else None
    return {
        "current_user": user,
        "is_admin": role == User.Role.ADMIN,
        "is_author": role == User.Role.AUTHOR,
    }


def project_context(request):
    """Данные, доступные всем шаблонам без дублирования во views."""
    return {
        "site_name": "Podcast Planner",
        "global_podcast_count": Podcast.objects.count(),
        "global_episode_count": Episode.objects.count(),
    }
