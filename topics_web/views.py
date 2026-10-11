"""Просмотр и добавление тем."""

from html import escape

from django.http import HttpResponse
from django.shortcuts import redirect

from homepage.auth import admin_required
from homepage.views import csrf_input, page
from models import Topic
from storage import load_topics, save_topics

TOPICS_FILE = "data/topics.json"


@admin_required
def topics(request):
    """Список тем и добавление новой темы."""
    topics_list = load_topics(TOPICS_FILE)
    message = ""

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            message = """
            <div class="alert alert-danger">
                Название темы не должно быть пустым.
            </div>
            """
        elif any(
            item.name.lower() == name.lower()
            for item in topics_list
        ):
            message = """
            <div class="alert alert-warning">
                Такая тема уже существует.
            </div>
            """
        else:
            next_id = max(
                (item.id for item in topics_list),
                default=0,
            ) + 1
            topics_list.append(Topic(next_id, name))
            save_topics(TOPICS_FILE, topics_list)
            return redirect("/topics/")

    items = "".join(
        f'<li class="list-group-item">#{item.id}: '
        f'{escape(item.name)}</li>'
        for item in topics_list
    )

    content = f"""
    <h1>Темы</h1>
    {message}

    <div class="row g-4">
        <div class="col-lg-7">
            <ul class="list-group shadow-sm">
                {items}
            </ul>
        </div>

        <div class="col-lg-5">
            <div class="card shadow-sm border-0">
                <div class="card-body">
                    <h2 class="h4">Добавить тему</h2>
                    <form method="post">
                        {csrf_input(request)}
                        <label class="form-label">
                            Название
                        </label>
                        <input class="form-control mb-3"
                               name="name"
                               required>
                        <button class="btn btn-primary">
                            Добавить
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    """

    return HttpResponse(page("Темы", content, request))
