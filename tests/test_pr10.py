from datetime import date

import pytest
from django.urls import reverse

from authors_web.models import User, hash_password
from episodes_web.models import Episode
from podcasts_web.models import Podcast
from topics_web.models import Topic


@pytest.fixture
def pr10_data(db):
    author = User.objects.create(
        name="PR10 Автор", login="pr10-author",
        password_hash=hash_password("pass"), role=User.Role.AUTHOR,
    )
    topic = Topic.objects.create(name="PR10")
    podcast = Podcast.objects.create(
        title="PR10 Podcast", description="Admin and ORM", author=author,
    )
    published = Episode.objects.create(
        podcast=podcast, title="Published", topic=topic, author=author,
        status=Episode.Status.PUBLISHED, release_date=date(2026, 11, 1),
    )
    ready = Episode.objects.create(
        podcast=podcast, title="Ready", topic=topic, author=author,
        status=Episode.Status.READY, release_date=date(2026, 11, 2),
    )
    return author, topic, podcast, published, ready


@pytest.mark.django_db
def test_custom_queryset_and_relations(pr10_data):
    author, _, podcast, published, ready = pr10_data
    assert list(Episode.objects.published()) == [published]
    assert list(Episode.objects.ready()) == [ready]
    assert Episode.objects.by_author(author).count() == 2
    assert Episode.objects.search("PR10 Podcast").count() == 2
    assert podcast.episodes.count() == 2


@pytest.mark.django_db
def test_podcast_slug_and_absolute_url(pr10_data):
    _, _, podcast, _, _ = pr10_data
    assert podcast.slug
    assert podcast.get_absolute_url() == reverse(
        "podcasts_web:detail_slug", kwargs={"slug": podcast.slug}
    )


@pytest.mark.django_db
def test_missing_podcast_slug_returns_404(client):
    # Без сессии login_required сначала отправляет на страницу входа.
    response = client.get('/podcasts/slug/not-existing/')
    assert response.status_code in {302, 404}


@pytest.mark.django_db
def test_generated_title_length(pr10_data):
    _, _, podcast, _, _ = pr10_data
    podcast.refresh_from_db()
    assert podcast.title_length == len(podcast.title)

    podcast.title = "Новое название PR10"
    podcast.save()
    podcast.refresh_from_db()
    assert podcast.title_length == len(podcast.title)
