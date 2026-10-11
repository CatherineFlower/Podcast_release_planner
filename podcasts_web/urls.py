from django.urls import path

from . import views

app_name = "podcasts_web"

urlpatterns = [
    path("", views.podcasts, name="podcasts"),
    path("<int:podcast_id>/", views.podcast_detail, name="detail"),
]
