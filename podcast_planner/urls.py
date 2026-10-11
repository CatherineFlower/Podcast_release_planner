"""Корневая маршрутизация проекта."""

from django.contrib import admin
from django.urls import include, path, re_path

from homepage import views as homepage_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("podcasts/", include("podcasts_web.urls")),
    path("episodes/", include("episodes_web.urls")),
    path("topics/", include("topics_web.urls")),
    path("authors/", include("authors_web.urls")),
    re_path(
        r"^(?P<path>.*)$",
        homepage_views.catch_all_404,
        name="catch_all_404",
    ),
]

# Пользовательский обработчик ошибки маршрутизации 404.

handler404 = "homepage.views.page_not_found"
