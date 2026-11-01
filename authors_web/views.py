"""View-функции авторов."""

from django.shortcuts import redirect, render

from homepage.auth import admin_required
from models import Author
from models.users import hash_password
from storage import load_users, save_users

USERS_FILE = "data/users.json"


@admin_required
def authors(request):
    """Показать авторов и добавить нового автора."""
    users = load_users(USERS_FILE)
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        if not name or not login or not password:
            error = "Заполните все поля."
        elif any(
            item.login == login
            for item in users
        ):
            error = "Такой логин уже используется."
        else:
            next_id = max(
                (item.id for item in users),
                default=0,
            ) + 1
            users.append(
                Author(
                    next_id,
                    name,
                    login,
                    hash_password(password),
                )
            )
            save_users(
                USERS_FILE,
                users,
            )
            return redirect("authors_web:authors")

    author_list = [
        item
        for item in users
        if isinstance(item, Author)
    ]

    return render(
        request,
        "authors_web/author_list.html",
        {
            "authors": author_list,
            "error": error,
        },
    )
