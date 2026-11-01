"""Темы из SQLite."""

from django.shortcuts import redirect, render

from db.repository import add_topic, get_topics
from homepage.auth import admin_required


@admin_required
def topics(request):
    error = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            error = "Название темы не должно быть пустым."
        elif not add_topic(name):
            error = "Такая тема уже существует."
        else:
            return redirect("topics_web:topics")

    return render(
        request,
        "topics_web/topic_list.html",
        {"topics": get_topics(), "error": error},
    )
