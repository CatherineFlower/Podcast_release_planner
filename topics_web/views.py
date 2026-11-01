"""View-функции тем."""

from django.shortcuts import redirect, render

from homepage.auth import admin_required
from models import Topic
from storage import load_topics, save_topics

TOPICS_FILE = "data/topics.json"


@admin_required
def topics(request):
    """Показать темы и добавить новую тему."""
    topics_list = load_topics(TOPICS_FILE)
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            error = "Название темы не должно быть пустым."
        elif any(
            item.name.lower() == name.lower()
            for item in topics_list
        ):
            error = "Такая тема уже существует."
        else:
            next_id = max(
                (item.id for item in topics_list),
                default=0,
            ) + 1
            topics_list.append(
                Topic(next_id, name)
            )
            save_topics(
                TOPICS_FILE,
                topics_list,
            )
            return redirect("topics_web:topics")

    return render(
        request,
        "topics_web/topic_list.html",
        {
            "topics": topics_list,
            "error": error,
        },
    )
