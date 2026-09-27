from pathlib import Path

from models import ReleaseStatus, Topic
from models.episodes import Episode
from models.podcasts import Podcast
from models.users import Author, hash_password
from storage import load_episodes, save_episodes


def test_episode_json_roundtrip(tmp_path: Path):
    author = Author(2, "Author", "author", hash_password("x"))
    podcast = Podcast(1, "Podcast", "Description", author)
    topic = Topic(1, "Python")
    episode = Episode(
        1,
        podcast,
        "Episode",
        topic,
        author,
        ReleaseStatus.READY,
        "2026-10-01",
    )

    path = tmp_path / "episodes.json"
    save_episodes(str(path), [episode])
    loaded = load_episodes(
        str(path),
        [podcast],
        [topic],
        [author],
    )

    assert len(loaded) == 1
    assert loaded[0].podcast is podcast
    assert loaded[0].author is author
