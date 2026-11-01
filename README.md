# Podcast Planner — ПР7: SQLite и SQL

В ПР7 к проекту ПР1–ПР6 добавлен отдельный реляционный слой хранения данных.
Django ORM не используется: веб-представления работают с SQLite напрямую через
стандартный модуль `sqlite3`.

## База данных

Файл предметной базы ПР7:

```text
data/podcast_planner.sqlite
```

Важно: корневой `db.sqlite3`, который Django может создать после `migrate`,
используется только внутренними компонентами Django (в частности, сессиями).
Предметные данные ПР7 хранятся именно в `data/podcast_planner.sqlite`.

Таблицы:

- `users(id, name, login, password_hash, role)`;
- `topics(id, name)`;
- `podcasts(id, title, description, author_id)`;
- `episodes(id, podcast_id, title, topic_id, author_id, status, release_date)`.

Первичные ключи: `id` каждой таблицы.

Внешние ключи:

- `podcasts.author_id -> users.id`;
- `episodes.podcast_id -> podcasts.id`;
- `episodes.topic_id -> topics.id`;
- `episodes.author_id -> users.id`.

Проверка внешних ключей включается при каждом подключении:

```python
conn.execute("PRAGMA foreign_keys = ON")
```

## Файлы ПР7

```text
db/
├── database.py     # подключение SQLite + sqlite3.Row
├── init_db.py      # выполнение schema.sql
├── import_json.py  # перенос JSON -> SQLite
└── repository.py   # SQL-функции веб-приложения

sql/
├── schema.sql      # CREATE TABLE, ключи, индексы
└── queries.sql     # 16 проверочных SQL-запросов
```

JSON-файлы ПР1–ПР6 сохранены как исходная реализация и источник импорта.

## Создание и заполнение базы

Из корня проекта:

```bash
python -m db.init_db
python -m db.import_json
```

Скрипт импорта можно повторить: перед импортом он очищает таблицы в порядке,
обратном внешним ключам, а затем загружает `users -> topics -> podcasts -> episodes`.

## SQL-запросы

`sql/queries.sql` содержит 16 запросов, включая:

- 2 выборки списков;
- несколько `WHERE`;
- несколько `JOIN`;
- `COUNT()`;
- `GROUP BY`;
- `HAVING`;
- `ORDER BY` и `LIMIT`;
- поиск по `LIKE`.

Проверить все демонстрационные запросы:

```bash
sqlite3 data/podcast_planner.sqlite < sql/queries.sql
```

## Параметризованные запросы

Пользовательские значения не вставляются в SQL через f-строки.
Например, вход выполняется так:

```python
conn.execute(
    "SELECT * FROM users WHERE login = ?",
    (login,),
)
```

Поиск выпусков передаёт строку, статус и даты отдельными параметрами `?`.

## Django и SQLite

В `db/database.py` установлено:

```python
conn.row_factory = sqlite3.Row
```

Поэтому Django view может обращаться к результатам по именам столбцов, а
шаблон — как к `episode.title`, `episode.podcast_title` и т. д.

Пользовательские сценарии SQLite:

- `/` — счётчики из SQL;
- `/podcasts/` — список подкастов из SQLite;
- `/podcasts/<id>/` — подкаст и связанные выпуски через SQL;
- `/episodes/` — список, поиск, фильтр по статусу и диапазону дат;
- `/episodes/<id>/` — JOIN-данные конкретного выпуска;
- `/statistics/` — агрегаты `COUNT`, `GROUP BY`;
- `/topics/` — темы SQLite;
- `/authors/` — авторы SQLite.

Добавление и изменение данных из веб-интерфейса также выполняются SQL-командами
`INSERT`, `UPDATE`, `DELETE` с параметрами.

## Авторизация

Администратор:

```text
admin / admin123
```

Авторы:

```text
anna / anna123
ivan / ivan123
maria / maria123
alex / alex123
elena / elena123
```

## Проверка

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv,.venv
python manage.py runserver
```

## Git

```bash
git add .
git commit -m "PR7: add SQLite database and SQL queries"
git push
```

Коммиты ПР7 должны начинаться с `PR7:`.
