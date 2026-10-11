"""Просмотр и добавление авторов."""

from html import escape

from django.http import HttpResponse
from django.shortcuts import redirect

from homepage.auth import admin_required
from homepage.views import csrf_input, page
from models import Author
from models.users import hash_password
from storage import load_users, save_users

USERS_FILE = "data/users.json"


@admin_required
def authors(request):
    """Список авторов и добавление автора."""
    users = load_users(USERS_FILE)
    message = ""

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        login = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        if not name or not login or not password:
            message = """
            <div class="alert alert-danger">
                Заполните все поля.
            </div>
            """
        elif any(item.login == login for item in users):
            message = """
            <div class="alert alert-warning">
                Такой логин уже используется.
            </div>
            """
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
            save_users(USERS_FILE, users)
            return redirect("/authors/")

    author_list = [
        item for item in users if isinstance(item, Author)
    ]

    rows = "".join(
        f"""
        <tr>
            <td>{item.id}</td>
            <td>{escape(item.name)}</td>
            <td>{escape(item.login)}</td>
        </tr>
        """
        for item in author_list
    )

    content = f"""
    <h1>Авторы компании</h1>
    {message}

    <div class="row g-4">
        <div class="col-lg-7">
            <div class="card table-card shadow-sm">
                <table class="table mb-0">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Имя</th>
                            <th>Логин</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>

        <div class="col-lg-5">
            <div class="card shadow-sm border-0">
                <div class="card-body">
                    <h2 class="h4">Добавить автора</h2>
                    <form method="post">
                        {csrf_input(request)}
                        <input class="form-control mb-2"
                               name="name"
                               placeholder="ФИО"
                               required>
                        <input class="form-control mb-2"
                               name="login"
                               placeholder="Логин"
                               required>
                        <input class="form-control mb-3"
                               name="password"
                               type="password"
                               placeholder="Пароль"
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

    return HttpResponse(page("Авторы", content, request))
