from models import ReleaseStatus, Topic
from models.episodes import (
    add_episode,
    filter_by_status,
)
from models.podcasts import Podcast
from models.users import Author, hash_password


def make_objects():
    author = Author(2, "Author", "author", hash_password("x"))
    podcast = Podcast(1, "Podcast", "Description", author)
    topic = Topic(1, "Python")
    return author, podcast, topic


def test_episode_creation_and_links():
    author, podcast, topic = make_objects()
    episodes = []
    episode = add_episode(
        episodes,
        podcast,
        "Episode",
        topic,
        author,
        ReleaseStatus.PLANNED,
        "2026-10-01",
    )
    assert episode.podcast is podcast
    assert episode.topic is topic
    assert episode.author is author


def test_change_status():
    author, podcast, topic = make_objects()
    episodes = []
    episode = add_episode(
        episodes,
        podcast,
        "Episode",
        topic,
        author,
        ReleaseStatus.PLANNED,
        "2026-10-01",
    )
    episode.change_status(ReleaseStatus.PUBLISHED)
    assert episode.is_published


def test_filter_by_status():
    author, podcast, topic = make_objects()
    episodes = []
    add_episode(
        episodes,
        podcast,
        "Episode",
        topic,
        author,
        ReleaseStatus.READY,
        "2026-10-01",
    )
    assert len(filter_by_status(episodes, ReleaseStatus.READY)) == 1
