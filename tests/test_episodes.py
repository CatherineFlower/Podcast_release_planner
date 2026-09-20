from episodes import add_episode, find_episodes, filter_by_status, update_status, delete_episode


def test_add_episode():
    data = []
    add_episode(data, "Выпуск 1", "Python", "planned", "2026-10-01")
    assert len(data) == 1


def test_find_episodes():
    data = []
    add_episode(data, "Про Python", "Разработка", "planned", "2026-10-01")
    assert len(find_episodes(data, "python")) == 1


def test_filter_by_status():
    data = []
    add_episode(data, "A", "Тема", "ready", "2026-10-01")
    assert len(filter_by_status(data, "ready")) == 1


def test_update_status():
    data = []
    add_episode(data, "A", "Тема", "planned", "2026-10-01")
    assert update_status(data, 1, "ready")
    assert data[0]["status"] == "ready"


def test_delete_episode():
    data = []
    add_episode(data, "A", "Тема", "planned", "2026-10-01")
    assert delete_episode(data, 1)
    assert data == []
