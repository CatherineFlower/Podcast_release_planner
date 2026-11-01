-- Podcast Planner: структура базы данных ПР7
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'author'))
);

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS podcasts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS episodes (
    id INTEGER PRIMARY KEY,
    podcast_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    topic_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (
        status IN ('idea', 'planned', 'recording', 'ready', 'published')
    ),
    release_date TEXT NOT NULL,
    FOREIGN KEY (podcast_id) REFERENCES podcasts(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (author_id) REFERENCES users(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_podcasts_author
ON podcasts(author_id);

CREATE INDEX IF NOT EXISTS idx_episodes_podcast
ON episodes(podcast_id);

CREATE INDEX IF NOT EXISTS idx_episodes_topic
ON episodes(topic_id);

CREATE INDEX IF NOT EXISTS idx_episodes_author
ON episodes(author_id);

CREATE INDEX IF NOT EXISTS idx_episodes_status
ON episodes(status);

CREATE INDEX IF NOT EXISTS idx_episodes_release_date
ON episodes(release_date);
