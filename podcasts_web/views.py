"""Подкасты: данные получают Django views напрямую из SQLite."""

from django.shortcuts import redirect, render

from db.repository import (
    add_podcast,
    get_authors,
    get_podcast,
    get_podcast_episodes,
    get_podcasts,
)
from homepage.auth import forbidden_response, login_required


@login_required
def podcasts(request):
    user = request.current_user

    if request.method == "POST":
        if user["role"] != "admin":
            return forbidden_response(request)
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        try:
            author_id = int(request.POST.get("author_id", "0"))
        except ValueError:
            author_id = 0
        if title and description and author_id:
            add_podcast(title, description, author_id)
        return redirect("podcasts_web:podcasts")

    author_id = user["id"] if user["role"] == "author" else None
    return render(
        request,
        "podcasts_web/podcast_list.html",
        {
            "podcasts": get_podcasts(author_id),
            "authors": get_authors(),
        },
    )


@login_required
def podcast_detail(request, podcast_id):
    user = request.current_user
    podcast = get_podcast(podcast_id)
    if (
        podcast is not None
        and user["role"] == "author"
        and podcast["author_id"] != user["id"]
    ):
        return forbidden_response(request)

    context = {
        "podcast": podcast,
        "podcast_episodes": (
            get_podcast_episodes(podcast_id)
            if podcast is not None
            else []
        ),
    }
    return render(
        request,
        "podcasts_web/podcast_detail.html",
        context,
        status=404 if podcast is None else 200,
    )
