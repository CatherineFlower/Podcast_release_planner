"""Темы выпусков через Django ORM."""

from django.shortcuts import redirect, render

from homepage.auth import admin_required

from .models import Topic


@admin_required
def topics(request):
    error = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            error = "Название темы не должно быть пустым."
        elif Topic.objects.filter(name__iexact=name).exists():
            error = "Такая тема уже существует."
        else:
            Topic.objects.create(name=name)
            return redirect("topics_web:topics")

    return render(
        request,
        "topics_web/topic_list.html",
        {"topics": Topic.objects.all(), "error": error},
    )
