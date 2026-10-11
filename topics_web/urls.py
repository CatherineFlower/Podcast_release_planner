from django.urls import path

from . import views

app_name = "topics_web"

urlpatterns = [
    path("", views.topics, name="topics"),
]
