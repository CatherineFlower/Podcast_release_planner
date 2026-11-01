# ПР7 — защита по таблице из 25 пунктов

Проект: «Система планирования выпусков подкастов».

## Перед защитой

### Запустить

```bash
python -m db.init_db
python -m db.import_json
python -m db.check_db
python manage.py check
pytest -v
python manage.py runserver
```

### Логин

```text
admin
admin123
```

### Открыть в PyCharm заранее

Двойной Shift → вставить путь:

1. `sql/schema.sql`
2. `sql/queries.sql`
3. `db/database.py`
4. `db/init_db.py`
5. `db/import_json.py`
6. `db/repository.py`
7. `data/users.json`
8. `data/podcasts.json`
9. `data/topics.json`
10. `data/episodes.json`
11. `podcasts_web/views.py`
12. `episodes_web/views.py`
13. `homepage/views.py`
14. `episodes_web/templates/episodes_web/episode_list.html`
15. `homepage/templates/homepage/statistics.html`
16. `README.md`

### Открыть в браузере

- `http://127.0.0.1:8000/podcasts/`
- `http://127.0.0.1:8000/podcasts/1/`
- `http://127.0.0.1:8000/episodes/`
- `http://127.0.0.1:8000/episodes/?status=published&sort=date`
- `http://127.0.0.1:8000/episodes/?q=Python`
- `http://127.0.0.1:8000/statistics/`

### Подготовить терминал SQLite

```bash
sqlite3 data/podcast_planner.sqlite
```

Полезные команды:

```sql
.tables
.schema users
.schema podcasts
.schema episodes
PRAGMA foreign_key_list(episodes);
```

---

## 1. Проектирование структуры базы данных

Открыть `sql/schema.sql`.

Сказать:

«В моём проекте четыре таблицы: `users`, `topics`, `podcasts`, `episodes`.
`users` хранит администратора и авторов, `topics` — темы, `podcasts` —
подкасты, `episodes` — выпуски. Подкаст связан с автором, а выпуск связан с
подкастом, темой и автором через внешние ключи».

---

## 2. Создание таблиц и связей

Показать `PRIMARY KEY` и `FOREIGN KEY` в `schema.sql`.

Сказать:

«`id INTEGER PRIMARY KEY` уникально определяет запись. Например,
`episodes.podcast_id` ссылается на `podcasts.id`, `topic_id` — на `topics.id`,
`author_id` — на `users.id`. Внешние ключи не дают создать выпуск со ссылкой
на несуществующий объект».

В SQLite можно выполнить:

```sql
PRAGMA foreign_key_list(episodes);
```

---

## 3. Создание базы и выполнение схемы

Показать `db/init_db.py` и `CREATE TABLE IF NOT EXISTS`.

В терминале:

```bash
python -m db.init_db
```

Сказать:

«Скрипт читает `schema.sql` и выполняет его через `executescript()`.
`IF NOT EXISTS` позволяет запускать схему повторно без ошибки существующей
таблицы».

---

## 4. Подключение к базе данных

Открыть `db/database.py`.

Показать:

```python
DB_PATH = BASE_DIR / "data" / "podcast_planner.sqlite"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")
```

Сказать:

«Путь строится от корня проекта, поэтому подключение всегда открывает нужный
файл. Проверить можно `SELECT COUNT(*) FROM podcasts` или вывести `DB_PATH`».

---

## 5. Импорт данных из JSON

Открыть `db/import_json.py`.

Показать `executemany()` и порядок:

```text
users → topics → podcasts → episodes
```

Сказать:

«Порядок важен из-за внешних ключей: сначала импортируются записи, на которые
ссылаются другие таблицы. Значения передаются через `?`, затем выполняется
`commit()`. При ошибке вызывается `rollback()`».

---

## 6. Проверка результатов импорта

В SQLite:

```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM topics;
SELECT COUNT(*) FROM podcasts;
SELECT COUNT(*) FROM episodes;
```

Сравнить с количеством объектов в соответствующих JSON.

Сказать:

«Если количество отличается, значит импорт выполнен не полностью либо часть
записей не прошла ограничения базы».

---

## 7. SELECT

В `queries.sql` показать запрос 1:

```sql
SELECT id, title, description, author_id
FROM podcasts
ORDER BY title;
```

Сказать:

«`SELECT` задаёт столбцы результата. Если оставить только `id, title`, в
результате не будет `description` и `author_id`, следовательно эти значения
нельзя будет вывести без дополнительного запроса».

---

## 8. WHERE

Показать запрос 3:

```sql
SELECT id, title, release_date, status
FROM episodes
WHERE status = 'published';
```

Поменять `published` на `ready`.

Сказать:

«`WHERE` фильтрует отдельные строки. При изменении условия меняется набор
выпусков в результате».

---

## 9. Фильтрация по состоянию

Тот же запрос со `status`.

Сказать:

«Статус — состояние выпуска. `published` включает только опубликованные,
`planned` — только запланированные. Остальные состояния исключаются».

В браузере можно показать:

`/episodes/?status=published`

---

## 10. JOIN

В `queries.sql` показать запрос 6.

Сказать:

«`episodes` хранит идентификаторы связанных объектов. JOIN соединяет выпуск с
`podcasts`, `topics`, `users`, поэтому результат содержит понятные названия
подкаста, темы и автора вместо одних ID».

---

## 11. Несколько условий

Открыть `db/repository.py` → `get_episodes()`.

Показать условия строки поиска, статуса и диапазона дат.

В браузере:

`/episodes/?status=published&date_from=2026-09-01&date_to=2026-10-31`

Сказать:

«Условия объединяются через AND. Если изменить дату или статус, состав
результата изменится».

---

## 12. COUNT()

Показать запрос 7/8:

```sql
SELECT COUNT(*) AS published_count
FROM episodes
WHERE status = 'published';
```

Сказать:

«COUNT подсчитывает число подходящих строк. Если подходящих строк нет,
`COUNT(*)` вернёт 0, а не пустой результат».

---

## 13. GROUP BY

Показать запрос 10:

```sql
SELECT podcasts.title, COUNT(episodes.id)
FROM podcasts
LEFT JOIN episodes ON podcasts.id = episodes.podcast_id
GROUP BY podcasts.id, podcasts.title;
```

Сказать:

«`GROUP BY` формирует отдельную группу для каждого подкаста, а `COUNT()`
вычисляется внутри каждой группы».

---

## 14. HAVING

Показать запрос 11:

```sql
HAVING COUNT(episodes.id) >= 7
```

Временно поменять `7` на `8`.

Сказать:

«`WHERE` фильтрует строки до группировки, а `HAVING` фильтрует уже готовые
группы после `GROUP BY`. Изменение порога меняет набор подкастов».

---

## 15. Параметризованные запросы

Открыть `db/repository.py`, например `get_user_by_login()`:

```python
conn.execute(
    "SELECT * FROM users WHERE login = ?",
    (login,),
)
```

И `get_episodes()`.

Сказать:

«Пользовательское значение передаётся отдельно от SQL-текста через `?`.
Подставлять ввод f-строкой нельзя: это смешивает данные с SQL-кодом и создаёт
риск SQL-инъекций».

---

## 16. Получение и обработка результатов SQL

Показать `db/database.py`:

```python
conn.row_factory = sqlite3.Row
```

и `repository.py` → `.fetchall()`.

Сказать:

«`sqlite3.Row` позволяет обращаться к результату по имени столбца:
`row['title']`, а в Django-шаблоне — `episode.title`, вместо индексов `row[1]`».

---

## 17. Отображение списка объектов

В браузере открыть `/podcasts/`.

В коде показать `podcasts_web/views.py`:

```python
"podcasts": get_podcasts(author_id)
```

и шаблон `podcast_list.html`.

Сказать:

«SQL возвращает строки SQLite, view кладёт их в context под ключом `podcasts`,
а шаблон выводит их циклом».

---

## 18. Отображение отфильтрованных записей

Открыть:

`/episodes/?status=published`

Сказать:

«Фильтрация выполняется SQL-условием `WHERE e.status = ?`, поэтому в шаблон
передаются уже отобранные строки».

---

## 19. Отображение связанных данных

Открыть `/episodes/1/`.

Показать `get_episode()` и поля:

```text
podcast_title
topic_name
author_name
```

Сказать:

«Эти значения приходят одной результирующей строкой JOIN из четырёх таблиц и
сразу используются шаблоном».

---

## 20. Поиск по пользовательским параметрам

Открыть `/episodes/` и ввести `Python`, выбрать статус или даты.

Показать в view:

```python
query = request.GET.get("q", "").strip()
```

и передачу в `get_episodes()`.

Сказать:

«GET-параметр приходит во view, затем передаётся отдельным параметром в SQL.
Результат возвращается на ту же страницу».

---

## 21. Статистика

Открыть `/statistics/`.

Показать `get_status_statistics()` и `get_podcast_statistics()`.

Сказать:

«Статистика считается в SQLite через `COUNT`, `GROUP BY`, `LEFT JOIN`, а view
передаёт агрегированные строки в шаблон. Python не пересчитывает весь список
выпусков вручную».

---

## 22. Передача результатов в шаблон

Показать `podcasts_web/views.py`:

```python
{"podcasts": get_podcasts(author_id)}
```

и шаблон:

```django
{% for podcast in podcasts %}
```

Сказать:

«Имена должны совпадать. Если во view назвать ключ `items`, а в шаблоне оставить
`podcasts`, SQL выполнится, но шаблон не увидит данные. Исправление — одинаковое
имя context-переменной».

---

## 23. Пустой результат

На `/episodes/` в поиск ввести, например:

```text
НЕСУЩЕСТВУЮЩИЙ_ВЫПУСК_999
```

Сказать:

«Запрос выполняется успешно и возвращает пустой список. Это не ошибка SQL.
Шаблон обрабатывает это через `{% empty %}` и показывает “Выпуски не найдены”».

---

## 24. Диагностика SQL-ошибок

В терминале SQLite намеренно выполнить:

```sql
SELECT wrong_column FROM podcasts;
```

Получить ошибку `no such column`.

Исправить:

```sql
SELECT title FROM podcasts;
```

Сказать:

«Если результат некорректный, сначала проверяю имена таблиц и столбцов,
`WHERE`, затем условия `JOIN`. SQL удобно сначала проверить напрямую в SQLite,
а затем переносить в Django».

---

## 25. Сквозная обработка запроса в Django

На примере поиска `Python`:

1. браузер отправляет `/episodes/?q=Python`;
2. `episodes_web/urls.py` выбирает view;
3. `episodes()` читает `request.GET`;
4. `get_episodes()` выполняет параметризованный SQL;
5. SQLite возвращает `sqlite3.Row`;
6. view передаёт `episodes` в context;
7. `episode_list.html` выводит результат;
8. браузер получает HTML.

Сказать:

«Если результат неверный, проверяю последовательно параметр запроса, SQL,
параметры `execute`, данные базы, context и шаблон».

---

## Что НЕ забыть показать, если преподаватель попросит дополнительно

`README.md`, проверки:

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv,.venv
```

и Git-коммит:

```text
PR7: add SQLite database and SQL queries
```
