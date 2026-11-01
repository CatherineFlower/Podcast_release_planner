"""Авторы из SQLite."""

from django.shortcuts import redirect, render

from db.repository import add_author, get_authors
from homepage.auth import admin_required
from models.users import hash_password


@admin_required
def authors(request):
    error = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")
        if not name or not login or not password:
            error = "Заполните все поля."
        elif not add_author(name, login, hash_password(password)):
            error = "Такой логин уже используется."
        else:
            return redirect("authors_web:authors")

    return render(
        request,
        "authors_web/author_list.html",
        {"authors": get_authors(), "error": error},
    )
