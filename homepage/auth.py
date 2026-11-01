"""Авторизация через пользователей, перенесённых в SQLite."""

from functools import wraps

from django.shortcuts import redirect, render

from db.repository import get_user_by_id

SESSION_USER_ID = "podcast_planner_user_id"


def get_current_user(request):
    if request is None:
        return None
    user_id = request.session.get(SESSION_USER_ID)
    if user_id is None:
        return None
    return get_user_by_id(user_id)


def forbidden_response(request):
    return render(request, "errors/403.html", status=403)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("homepage:login")
        request.current_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if user is None:
            return redirect("homepage:login")
        if user["role"] != "admin":
            return forbidden_response(request)
        request.current_user = user
        return view_func(request, *args, **kwargs)
    return wrapper
