"""Тесты функций работы с подкастами."""

from podcasts import (
    add_podcast,
    find_podcasts,
    podcast_exists,
    sort_podcasts_by_title,
)


def test_add_podcast():
    podcasts = []
    podcast = add_podcast(podcasts, "Tech Talk", "О технологиях")
    assert podcast["id"] == 1
    assert len(podcasts) == 1


def test_find_podcasts():
    podcasts = []
    add_podcast(podcasts, "Python Talks", "О Python")
    assert len(find_podcasts(podcasts, "python")) == 1


def test_sort_podcasts_by_title():
    podcasts = []
    add_podcast(podcasts, "Z Podcast", "")
    add_podcast(podcasts, "A Podcast", "")
    result = sort_podcasts_by_title(podcasts)
    assert result[0]["title"] == "A Podcast"


def test_podcast_exists():
    podcasts = []
    add_podcast(podcasts, "Podcast", "")
    assert podcast_exists(podcasts, 1)
