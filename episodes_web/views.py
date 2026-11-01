"""Выпуски: SELECT, WHERE, JOIN и параметризованный поиск SQLite."""

from django.shortcuts import redirect, render

from db.repository import (
    add_episode,
    delete_episode,
    get_authors,
    get_episode,
    get_episodes,
    get_podcasts,
    get_topics,
    update_episode_status,
)
from homepage.auth import forbidden_response, login_required
from models import ReleaseStatus


@login_required
def episodes(request):
    user = request.current_user

    if request.method == "POST":
        if user["role"] != "admin":
            return forbidden_response(request)
        try:
            podcast_id = int(request.POST.get("podcast_id", "0"))
            topic_id = int(request.POST.get("topic_id", "0"))
            author_id = int(request.POST.get("author_id", "0"))
        except ValueError:
            return redirect("episodes_web:episodes")

        title = request.POST.get("title", "").strip()
        status = request.POST.get("status", "").strip()
        release_date = request.POST.get("release_date", "").strip()
        if (
            title
            and status in ReleaseStatus.values()
            and release_date
            and podcast_id
            and topic_id
            and author_id
        ):
            add_episode(
                podcast_id,
                title,
                topic_id,
                author_id,
                status,
                release_date,
            )
        return redirect("episodes_web:episodes")

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    sort_value = request.GET.get("sort", "").strip()
    author_id = user["id"] if user["role"] == "author" else None

    return render(
        request,
        "episodes_web/episode_list.html",
        {
            "episodes": get_episodes(
                query=query,
                status=status,
                date_from=date_from,
                date_to=date_to,
                author_id=author_id,
                sort_by_date=sort_value == "date",
            ),
            "podcasts": get_podcasts(),
            "topics": get_topics(),
            "authors": get_authors(),
            "statuses": list(ReleaseStatus),
            "query": query,
            "selected_status": status,
            "date_from": date_from,
            "date_to": date_to,
            "selected_sort": sort_value,
        },
    )


@login_required
def episode_detail(request, episode_id):
    user = request.current_user
    episode = get_episode(episode_id)

    if (
        episode is not None
        and user["role"] == "author"
        and episode["author_id"] != user["id"]
    ):
        return forbidden_response(request)

    if episode is not None and request.method == "POST":
        if user["role"] != "admin":
            return forbidden_response(request)
        action = request.POST.get("action", "")
        if action == "status":
            status = request.POST.get("status", "")
            if status in ReleaseStatus.values():
                update_episode_status(episode_id, status)
        elif action == "delete":
            delete_episode(episode_id)
            return redirect("episodes_web:episodes")
        return redirect("episodes_web:detail", episode_id=episode_id)

    return render(
        request,
        "episodes_web/episode_detail.html",
        {
            "episode": episode,
            "statuses": list(ReleaseStatus),
        },
        status=404 if episode is None else 200,
    )
