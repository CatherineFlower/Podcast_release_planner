from django.urls import path

from . import views

app_name = "authors_web"

urlpatterns = [
    path("", views.authors, name="authors"),
]
