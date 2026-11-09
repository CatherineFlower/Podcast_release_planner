"""Авторы компании через Django ORM."""

from django.db import IntegrityError
from django.shortcuts import redirect, render

from homepage.auth import admin_required

from .models import User, hash_password


@admin_required
def authors(request):
    error = None
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")
        if not name or not login or not password:
            error = "Заполните все поля."
        elif User.objects.filter(login=login).exists():
            error = "Такой логин уже используется."
        else:
            try:
                User.objects.create(
                    name=name,
                    login=login,
                    password_hash=hash_password(password),
                    role=User.Role.AUTHOR,
                )
            except IntegrityError:
                error = "Не удалось создать автора."
            else:
                return redirect("authors_web:authors")

    return render(
        request,
        "authors_web/author_list.html",
        {
            "authors": User.objects.filter(
                role=User.Role.AUTHOR
            ).order_by("name"),
            "error": error,
        },
    )
