from django.urls import path

from . import views

app_name = "episodes_web"

urlpatterns = [
    path("", views.episodes, name="episodes"),
    path("<int:episode_id>/", views.episode_detail, name="detail"),
]
