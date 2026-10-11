"""Маршруты общей части сайта."""

from django.urls import path

from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("statistics/", views.statistics, name="statistics"),
]
