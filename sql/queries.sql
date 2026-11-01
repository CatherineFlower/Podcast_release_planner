-- Podcast Planner: проверенные SQL-запросы ПР7
-- Минимум выполнен с запасом: SELECT, WHERE, JOIN, агрегаты, GROUP BY.

-- 1. SELECT: список всех подкастов
SELECT id, title, description, author_id
FROM podcasts
ORDER BY title;

-- 2. SELECT: список всех тем
SELECT id, name
FROM topics
ORDER BY name;

-- 3. WHERE: только опубликованные выпуски
SELECT id, title, release_date, status
FROM episodes
WHERE status = 'published'
ORDER BY release_date DESC;

-- 4. WHERE: выпуски после заданной даты
SELECT id, title, release_date
FROM episodes
WHERE release_date >= '2026-11-01'
ORDER BY release_date;

-- 5. JOIN: подкасты вместе с авторами
SELECT
    podcasts.id,
    podcasts.title,
    users.name AS author_name
FROM podcasts
JOIN users ON podcasts.author_id = users.id
ORDER BY podcasts.title;

-- 6. JOIN: полная информация о выпусках из четырёх таблиц
SELECT
    episodes.id,
    episodes.title,
    podcasts.title AS podcast_title,
    topics.name AS topic_name,
    users.name AS author_name,
    episodes.status,
    episodes.release_date
FROM episodes
JOIN podcasts ON episodes.podcast_id = podcasts.id
JOIN topics ON episodes.topic_id = topics.id
JOIN users ON episodes.author_id = users.id
ORDER BY episodes.release_date;

-- 7. Агрегат: общее количество выпусков
SELECT COUNT(*) AS episodes_count
FROM episodes;

-- 8. Агрегат: количество опубликованных выпусков
SELECT COUNT(*) AS published_count
FROM episodes
WHERE status = 'published';

-- 9. GROUP BY: количество выпусков по статусам
SELECT status, COUNT(*) AS episodes_count
FROM episodes
GROUP BY status
ORDER BY episodes_count DESC;

-- 10. GROUP BY + JOIN: количество выпусков по подкастам
SELECT
    podcasts.id,
    podcasts.title,
    COUNT(episodes.id) AS episodes_count
FROM podcasts
LEFT JOIN episodes ON podcasts.id = episodes.podcast_id
GROUP BY podcasts.id, podcasts.title
ORDER BY episodes_count DESC, podcasts.title;

-- 11. HAVING: подкасты, у которых не менее 7 выпусков
SELECT
    podcasts.title,
    COUNT(episodes.id) AS episodes_count
FROM podcasts
JOIN episodes ON podcasts.id = episodes.podcast_id
GROUP BY podcasts.id, podcasts.title
HAVING COUNT(episodes.id) >= 7
ORDER BY episodes_count DESC;

-- 12. HAVING: авторы, у которых не менее 10 выпусков
SELECT
    users.name AS author_name,
    COUNT(episodes.id) AS episodes_count
FROM users
JOIN episodes ON users.id = episodes.author_id
WHERE users.role = 'author'
GROUP BY users.id, users.name
HAVING COUNT(episodes.id) >= 10
ORDER BY episodes_count DESC;

-- 13. WHERE + LIKE + JOIN: поиск выпусков по слову «Python»
SELECT
    episodes.title,
    podcasts.title AS podcast_title,
    topics.name AS topic_name
FROM episodes
JOIN podcasts ON episodes.podcast_id = podcasts.id
JOIN topics ON episodes.topic_id = topics.id
WHERE
    episodes.title LIKE '%Python%'
    OR podcasts.title LIKE '%Python%'
    OR topics.name LIKE '%Python%'
ORDER BY episodes.release_date;

-- 14. ORDER BY + LIMIT: пять ближайших выпусков
SELECT id, title, release_date, status
FROM episodes
WHERE release_date >= '2026-10-31'
ORDER BY release_date
LIMIT 5;

-- 15. JOIN + WHERE: выпуски автора Анны Смирновой
SELECT
    episodes.title,
    podcasts.title AS podcast_title,
    episodes.status,
    episodes.release_date
FROM episodes
JOIN podcasts ON episodes.podcast_id = podcasts.id
JOIN users ON episodes.author_id = users.id
WHERE users.login = 'anna'
ORDER BY episodes.release_date;

-- 16. GROUP BY + агрегат: количество выпусков по авторам
SELECT
    users.name AS author_name,
    COUNT(episodes.id) AS episodes_count
FROM users
LEFT JOIN episodes ON users.id = episodes.author_id
WHERE users.role = 'author'
GROUP BY users.id, users.name
ORDER BY episodes_count DESC, users.name;
