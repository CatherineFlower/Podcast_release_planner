from django.urls import path
from . import views

app_name = "podcasts_web"

urlpatterns = [
    path("", views.podcasts, name="podcasts"),
    path("<int:podcast_id>/", views.podcast_detail, name="detail"),
    path("slug/<slug:slug>/",
         views.podcast_detail_by_slug,
         name="detail_slug"),
]
