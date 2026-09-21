"""Тесты функций работы с выпусками."""

from episodes import (
    add_episode,
    delete_episode,
    filter_by_status,
    find_episodes,
    get_statistics,
    sort_by_release_date,
    update_status,
)


def test_add_episode():
    episodes = []
    episode = add_episode(
        episodes,
        1,
        "Первый выпуск",
        1,
        "planned",
        "2026-10-01",
    )
    assert episode["id"] == 1
    assert len(episodes) == 1


def test_find_episodes():
    episodes = []
    add_episode(episodes, 1, "Про Python", 1, "planned", "2026-10-01")
    assert len(find_episodes(episodes, "python")) == 1


def test_filter_by_status():
    episodes = []
    add_episode(episodes, 1, "A", 1, "ready", "2026-10-01")
    add_episode(episodes, 1, "B", 1, "planned", "2026-10-02")
    assert len(filter_by_status(episodes, "ready")) == 1


def test_sort_by_release_date():
    episodes = []
    add_episode(episodes, 1, "Позже", 1, "planned", "2026-10-20")
    add_episode(episodes, 1, "Раньше", 1, "planned", "2026-10-01")
    result = sort_by_release_date(episodes)
    assert result[0]["title"] == "Раньше"


def test_update_status():
    episodes = []
    add_episode(episodes, 1, "A", 1, "planned", "2026-10-01")
    assert update_status(episodes, 1, "ready")
    assert episodes[0]["status"] == "ready"


def test_delete_episode():
    episodes = []
    add_episode(episodes, 1, "A", 1, "planned", "2026-10-01")
    assert delete_episode(episodes, 1)
    assert episodes == []


def test_statistics():
    episodes = []
    add_episode(episodes, 1, "A", 1, "ready", "2026-10-01")
    add_episode(episodes, 1, "B", 1, "ready", "2026-10-02")
    assert get_statistics(episodes)["ready"] == 2
