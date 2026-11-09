"""Выпуски: фильтрация, сортировка и пагинация через Django ORM."""

from datetime import date

from django.core.paginator import Paginator
from django.db.models import Case, CharField, F, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from authors_web.models import User
from homepage.auth import forbidden_response, login_required
from podcasts_web.models import Podcast
from topics_web.models import Topic

from .models import Episode

SORT_FIELDS = {
    "date": "release_date",
    "date_desc": "-release_date",
    "title": "title",
    "podcast": "podcast__title",
}


def _parse_date(value: str):
    if not value:
        return None, None
    try:
        return date.fromisoformat(value), None
    except ValueError:
        return None, f"Некорректная дата: {value}"


def _status_title_expression():
    return Case(
        When(status=Episode.Status.IDEA, then=Value("Идея")),
        When(status=Episode.Status.PLANNED, then=Value("Запланирован")),
        When(status=Episode.Status.RECORDING, then=Value("Идет запись")),
        When(status=Episode.Status.READY, then=Value("Готов к публикации")),
        When(status=Episode.Status.PUBLISHED, then=Value("Опубликован")),
        default=Value("Неизвестный статус"),
        output_field=CharField(),
    )


@login_required
def episodes(request):
    user = request.current_user

    if request.method == "POST":
        if user.role != User.Role.ADMIN:
            return forbidden_response(request)
        try:
            podcast_id = int(request.POST.get("podcast_id", "0"))
            topic_id = int(request.POST.get("topic_id", "0"))
            author_id = int(request.POST.get("author_id", "0"))
        except ValueError:
            return redirect("episodes_web:episodes")

        title = request.POST.get("title", "").strip()
        status = request.POST.get("status", "").strip()
        release_date, _ = _parse_date(
            request.POST.get("release_date", "").strip()
        )
        if title and status in Episode.Status.values and release_date:
            podcast = Podcast.objects.filter(pk=podcast_id).first()
            topic = Topic.objects.filter(pk=topic_id).first()
            author = User.objects.filter(
                pk=author_id,
                role=User.Role.AUTHOR,
            ).first()
            if podcast and topic and author:
                Episode.objects.create(
                    podcast=podcast,
                    title=title,
                    topic=topic,
                    author=author,
                    status=status,
                    release_date=release_date,
                )
        return redirect("episodes_web:episodes")

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    date_from_raw = request.GET.get("date_from", "").strip()
    date_to_raw = request.GET.get("date_to", "").strip()
    sort_value = request.GET.get("sort", "date").strip()

    date_from, error_from = _parse_date(date_from_raw)
    date_to, error_to = _parse_date(date_to_raw)
    filter_error = error_from or error_to

    queryset = Episode.objects.select_related(
        "podcast", "topic", "author"
    )
    if user.role == User.Role.AUTHOR:
        queryset = queryset.filter(author=user)

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(podcast__title__icontains=query)
            | Q(topic__name__icontains=query)
            | Q(author__name__icontains=query)
        )
    if status in Episode.Status.values:
        queryset = queryset.filter(status=status)
    if date_from is not None:
        queryset = queryset.filter(release_date__gte=date_from)
    if date_to is not None:
        queryset = queryset.filter(release_date__lte=date_to)

    order_field = SORT_FIELDS.get(sort_value, "release_date")
    queryset = queryset.order_by(order_field, "pk")

    # Для списка получаем только действительно нужные шаблону поля.
    rows = (
        queryset.annotate(
            podcast_title=F("podcast__title"),
            topic_name=F("topic__name"),
            author_name=F("author__name"),
            status_title=_status_title_expression(),
        )
        .values(
            "id",
            "title",
            "podcast_id",
            "podcast_title",
            "topic_name",
            "author_name",
            "status",
            "status_title",
            "release_date",
        )
    )

    paginator = Paginator(rows, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    params = request.GET.copy()
    params.pop("page", None)

    return render(
        request,
        "episodes_web/episode_list.html",
        {
            "episodes": page_obj.object_list,
            "page_obj": page_obj,
            "query_params": params.urlencode(),
            "podcasts": Podcast.objects.order_by("title"),
            "topics": Topic.objects.order_by("name"),
            "authors": User.objects.filter(
                role=User.Role.AUTHOR
            ).order_by("name"),
            "statuses": Episode.Status,
            "sort_options": SORT_FIELDS,
            "query": query,
            "selected_status": status,
            "date_from": date_from_raw,
            "date_to": date_to_raw,
            "selected_sort": sort_value,
            "filter_error": filter_error,
        },
    )


@login_required
def episode_detail(request, episode_id):
    user = request.current_user
    episode = get_object_or_404(
        Episode.objects.select_related("podcast", "topic", "author"),
        pk=episode_id,
    )

    if user.role == User.Role.AUTHOR and episode.author_id != user.pk:
        return forbidden_response(request)

    if request.method == "POST":
        if user.role != User.Role.ADMIN:
            return forbidden_response(request)
        action = request.POST.get("action", "")
        if action == "status":
            status = request.POST.get("status", "")
            if status in Episode.Status.values:
                episode.change_status(status)
        elif action == "delete":
            episode.delete()
            return redirect("episodes_web:episodes")
        return redirect("episodes_web:detail", episode_id=episode.pk)

    return render(
        request,
        "episodes_web/episode_detail.html",
        {"episode": episode, "statuses": Episode.Status},
    )
