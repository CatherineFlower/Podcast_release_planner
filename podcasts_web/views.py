"""Подкасты: получение и изменение данных средствами Django ORM."""

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from authors_web.models import User
from homepage.auth import forbidden_response, login_required

from .models import Podcast


@login_required
def podcasts(request):
    user = request.current_user

    if request.method == "POST":
        if user.role != User.Role.ADMIN:
            return forbidden_response(request)
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        try:
            author_id = int(request.POST.get("author_id", "0"))
        except ValueError:
            author_id = 0
        author = User.objects.filter(
            pk=author_id,
            role=User.Role.AUTHOR,
        ).first()
        if title and description and author is not None:
            Podcast.objects.create(
                title=title,
                description=description,
                author=author,
            )
        return redirect("podcasts_web:podcasts")

    queryset = (
        Podcast.objects.select_related("author")
        .annotate(episode_count=Count("episodes"))
        .order_by("title", "pk")
    )
    if user.role == User.Role.AUTHOR:
        queryset = queryset.filter(author=user)

    return render(
        request,
        "podcasts_web/podcast_list.html",
        {
            "podcasts": queryset,
            "authors": User.objects.filter(
                role=User.Role.AUTHOR
            ).order_by("name"),
        },
    )


@login_required
def podcast_detail(request, podcast_id):
    user = request.current_user
    queryset = Podcast.objects.select_related("author").annotate(
        episode_count=Count("episodes")
    )
    podcast = get_object_or_404(queryset, pk=podcast_id)

    if user.role == User.Role.AUTHOR and podcast.author_id != user.pk:
        return forbidden_response(request)

    podcast_episodes = (
        podcast.episodes.select_related("topic", "author")
        .order_by("release_date", "pk")
    )
    return render(
        request,
        "podcasts_web/podcast_detail.html",
        {
            "podcast": podcast,
            "podcast_episodes": podcast_episodes,
        },
    )


@login_required
def podcast_detail_by_slug(request, slug):
    """Подробная страница по slug; используется get_absolute_url()."""
    user = request.current_user
    queryset = Podcast.objects.select_related("author").annotate(
        episode_count=Count("episodes")
    )
    podcast = get_object_or_404(queryset, slug=slug)
    if user.role == User.Role.AUTHOR and podcast.author_id != user.pk:
        return forbidden_response(request)
    podcast_episodes = podcast.episodes.select_related(
        "topic", "author"
    ).order_by("release_date", "pk")
    return render(
        request,
        "podcasts_web/podcast_detail.html",
        {"podcast": podcast, "podcast_episodes": podcast_episodes},
    )
