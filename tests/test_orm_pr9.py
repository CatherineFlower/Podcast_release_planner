"""Ключевые проверки моделей и ORM ПР9."""

from datetime import date

import pytest
from django.db.models import Count

from authors_web.models import User, hash_password
from episodes_web.models import Episode
from podcasts_web.models import Podcast
from topics_web.models import Topic


@pytest.fixture
def orm_data(db):
    author = User.objects.create(
        name="Тестовый автор",
        login="orm-author",
        password_hash=hash_password("pass"),
        role=User.Role.AUTHOR,
    )
    topic = Topic.objects.create(name="ORM")
    podcast = Podcast.objects.create(
        title="ORM Podcast",
        description="Test",
        author=author,
    )
    episode = Episode.objects.create(
        podcast=podcast,
        title="ORM Episode",
        topic=topic,
        author=author,
        status=Episode.Status.PLANNED,
        release_date=date(2026, 11, 10),
    )
    return author, topic, podcast, episode


@pytest.mark.django_db
def test_relations_and_select_related(orm_data):
    author, topic, podcast, episode = orm_data
    loaded = Episode.objects.select_related(
        "podcast", "topic", "author"
    ).get(pk=episode.pk)
    assert loaded.podcast == podcast
    assert loaded.topic == topic
    assert loaded.author == author
    assert list(podcast.episodes.all()) == [episode]


@pytest.mark.django_db
def test_filter_exclude_and_annotation(orm_data):
    _, _, podcast, episode = orm_data
    assert Episode.objects.filter(
        podcast__title__icontains="orm"
    ).count() == 1
    assert Episode.objects.exclude(
        status=Episode.Status.PUBLISHED
    ).count() == 1
    row = Podcast.objects.annotate(
        episode_count=Count("episodes")
    ).get(pk=podcast.pk)
    assert row.episode_count == 1


@pytest.mark.django_db
def test_update_and_delete(orm_data):
    _, _, _, episode = orm_data
    episode.change_status(Episode.Status.READY)
    assert Episode.objects.get(pk=episode.pk).status == Episode.Status.READY
    episode.delete()
    assert not Episode.objects.filter(pk=episode.pk).exists()
