"""Тесты функций работы с темами."""

from topics import add_topic, find_topics, topic_exists


def test_add_topic_without_duplicate():
    topics = []
    first = add_topic(topics, "Python")
    second = add_topic(topics, "python")
    assert first["id"] == second["id"]
    assert len(topics) == 1


def test_find_topics():
    topics = []
    add_topic(topics, "Backend")
    assert len(find_topics(topics, "back")) == 1


def test_topic_exists():
    topics = []
    add_topic(topics, "Разработка")
    assert topic_exists(topics, 1)
