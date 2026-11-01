"""SQL-функции предметной области Podcast Planner."""

from .database import get_connection

STATUS_TITLES = {
    "idea": "Идея",
    "planned": "Запланирован",
    "recording": "Идет запись",
    "ready": "Готов к публикации",
    "published": "Опубликован",
}


def _status_case(alias: str = "e") -> str:
    """SQL CASE с человекочитаемым названием статуса."""
    return f"""
        CASE {alias}.status
            WHEN 'idea' THEN 'Идея'
            WHEN 'planned' THEN 'Запланирован'
            WHEN 'recording' THEN 'Идет запись'
            WHEN 'ready' THEN 'Готов к публикации'
            WHEN 'published' THEN 'Опубликован'
        END
    """


def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()


def get_user_by_login(login: str):
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE login = ?",
            (login,),
        ).fetchone()
    finally:
        conn.close()


def get_authors():
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT id, name, login, role
            FROM users
            WHERE role = 'author'
            ORDER BY name
            """
        ).fetchall()
    finally:
        conn.close()


def add_author(name: str, login: str, password_hash: str) -> bool:
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT 1 FROM users WHERE login = ?",
            (login,),
        ).fetchone()
        if exists:
            return False
        conn.execute(
            """
            INSERT INTO users (name, login, password_hash, role)
            VALUES (?, ?, ?, 'author')
            """,
            (name, login, password_hash),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_topics():
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT id, name FROM topics ORDER BY name"
        ).fetchall()
    finally:
        conn.close()


def add_topic(name: str) -> bool:
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT 1 FROM topics WHERE LOWER(name) = LOWER(?)",
            (name,),
        ).fetchone()
        if exists:
            return False
        conn.execute(
            "INSERT INTO topics (name) VALUES (?)",
            (name,),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_podcasts(author_id: int | None = None):
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT
                p.id,
                p.title,
                p.description,
                p.author_id,
                u.name AS author_name,
                COUNT(e.id) AS episode_count
            FROM podcasts AS p
            JOIN users AS u ON p.author_id = u.id
            LEFT JOIN episodes AS e ON e.podcast_id = p.id
            WHERE (? IS NULL OR p.author_id = ?)
            GROUP BY p.id, p.title, p.description,
                     p.author_id, u.name
            ORDER BY p.title
            """,
            (author_id, author_id),
        ).fetchall()
    finally:
        conn.close()


def get_podcast(podcast_id: int):
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT
                p.id,
                p.title,
                p.description,
                p.author_id,
                u.name AS author_name
            FROM podcasts AS p
            JOIN users AS u ON p.author_id = u.id
            WHERE p.id = ?
            """,
            (podcast_id,),
        ).fetchone()
    finally:
        conn.close()


def add_podcast(title: str, description: str, author_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO podcasts (title, description, author_id)
            VALUES (?, ?, ?)
            """,
            (title, description, author_id),
        )
        conn.commit()
    finally:
        conn.close()


def _episode_select() -> str:
    return f"""
        SELECT
            e.id,
            e.podcast_id,
            e.title,
            e.topic_id,
            e.author_id,
            e.status,
            {_status_case('e')} AS status_title,
            e.release_date,
            p.title AS podcast_title,
            t.name AS topic_name,
            u.name AS author_name
        FROM episodes AS e
        JOIN podcasts AS p ON e.podcast_id = p.id
        JOIN topics AS t ON e.topic_id = t.id
        JOIN users AS u ON e.author_id = u.id
    """


def get_episodes(
    query: str = "",
    status: str = "",
    date_from: str = "",
    date_to: str = "",
    author_id: int | None = None,
    sort_by_date: bool = False,
):
    pattern = f"%{query}%"
    order_sql = (
        "ORDER BY e.release_date, e.id"
        if sort_by_date
        else "ORDER BY e.id"
    )
    sql = _episode_select() + f"""
        WHERE (
            ? = ''
            OR e.title LIKE ? COLLATE NOCASE
            OR p.title LIKE ? COLLATE NOCASE
            OR t.name LIKE ? COLLATE NOCASE
        )
        AND (? = '' OR e.status = ?)
        AND (? = '' OR e.release_date >= ?)
        AND (? = '' OR e.release_date <= ?)
        AND (? IS NULL OR e.author_id = ?)
        {order_sql}
    """
    params = (
        query, pattern, pattern, pattern,
        status, status,
        date_from, date_from,
        date_to, date_to,
        author_id, author_id,
    )
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def get_episode(episode_id: int):
    conn = get_connection()
    try:
        return conn.execute(
            _episode_select() + " WHERE e.id = ?",
            (episode_id,),
        ).fetchone()
    finally:
        conn.close()


def get_podcast_episodes(podcast_id: int):
    conn = get_connection()
    try:
        return conn.execute(
            _episode_select()
            + " WHERE e.podcast_id = ? ORDER BY e.release_date",
            (podcast_id,),
        ).fetchall()
    finally:
        conn.close()


def add_episode(
    podcast_id: int,
    title: str,
    topic_id: int,
    author_id: int,
    status: str,
    release_date: str,
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO episodes (
                podcast_id, title, topic_id,
                author_id, status, release_date
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                podcast_id,
                title,
                topic_id,
                author_id,
                status,
                release_date,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def update_episode_status(episode_id: int, status: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE episodes SET status = ? WHERE id = ?",
            (status, episode_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_episode(episode_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "DELETE FROM episodes WHERE id = ?",
            (episode_id,),
        )
        conn.commit()
    finally:
        conn.close()


def get_dashboard(author_id: int | None = None) -> dict:
    conn = get_connection()
    try:
        podcast_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM podcasts
            WHERE (? IS NULL OR author_id = ?)
            """,
            (author_id, author_id),
        ).fetchone()[0]
        episode_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM episodes
            WHERE (? IS NULL OR author_id = ?)
            """,
            (author_id, author_id),
        ).fetchone()[0]
        published_count = conn.execute(
            """
            SELECT COUNT(*)
            FROM episodes
            WHERE status = 'published'
              AND (? IS NULL OR author_id = ?)
            """,
            (author_id, author_id),
        ).fetchone()[0]
        topic_count = conn.execute(
            "SELECT COUNT(*) FROM topics"
        ).fetchone()[0]
        author_count = conn.execute(
            "SELECT COUNT(*) FROM users WHERE role = 'author'"
        ).fetchone()[0]
    finally:
        conn.close()
    return {
        "podcast_count": podcast_count,
        "episode_count": episode_count,
        "published_count": published_count,
        "topic_count": topic_count,
        "author_count": author_count,
    }


def get_status_statistics(author_id: int | None = None):
    conn = get_connection()
    try:
        rows = conn.execute(
            f"""
            SELECT
                e.status,
                {_status_case('e')} AS status_title,
                COUNT(*) AS episodes_count
            FROM episodes AS e
            WHERE (? IS NULL OR e.author_id = ?)
            GROUP BY e.status
            ORDER BY episodes_count DESC
            """,
            (author_id, author_id),
        ).fetchall()
        total = sum(row["episodes_count"] for row in rows)
        return [
            {
                "status": row["status"],
                "title": row["status_title"],
                "count": row["episodes_count"],
                "percent": (
                    f"{row['episodes_count'] / total * 100:.1f}"
                    if total
                    else "0.0"
                ),
            }
            for row in rows
        ]
    finally:
        conn.close()


def get_podcast_statistics(author_id: int | None = None):
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT
                p.id,
                p.title,
                COUNT(e.id) AS episodes_count,
                SUM(CASE WHEN e.status = 'published' THEN 1 ELSE 0 END)
                    AS published_count
            FROM podcasts AS p
            LEFT JOIN episodes AS e ON e.podcast_id = p.id
            WHERE (? IS NULL OR p.author_id = ?)
            GROUP BY p.id, p.title
            ORDER BY episodes_count DESC, p.title
            """,
            (author_id, author_id),
        ).fetchall()
    finally:
        conn.close()
