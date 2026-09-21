"""Функции для работы с темами выпусков."""


def add_topic(topics: list[dict], name: str) -> dict:
    """Добавить новую тему, если такой темы еще нет."""
    normalized = name.strip()
    for topic in topics:
        if topic["name"].lower() == normalized.lower():
            return topic

    topic = {
        "id": max((item["id"] for item in topics), default=0) + 1,
        "name": normalized,
    }
    topics.append(topic)
    return topic


def find_topics(topics: list[dict], query: str) -> list[dict]:
    """Найти темы по подстроке."""
    query = query.lower()
    return [
        topic
        for topic in topics
        if query in topic["name"].lower()
    ]


def topic_exists(topics: list[dict], topic_id: int) -> bool:
    """Проверить существование темы по идентификатору."""
    return any(topic["id"] == topic_id for topic in topics)
