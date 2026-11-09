# Podcast Planner — ПР9

ПР9 переводит слой доступа к данным проекта с ручного SQL/sqlite3 на Django ORM.
Веб-интерфейс, шаблоны, авторизация и пользовательские сценарии предыдущих работ сохранены.

## ORM-модели

- `authors_web.models.User` — пользователь компании (`admin` / `author`);
- `topics_web.models.Topic` — тема выпуска;
- `podcasts_web.models.Podcast` — подкаст, `ForeignKey` на автора;
- `episodes_web.models.Episode` — выпуск, `ForeignKey` на подкаст, тему и автора.

Для внешних ключей используется `on_delete=models.PROTECT`, чтобы связанные данные не удалялись случайно. Обратные связи задаются через `related_name`.

## Две базы в ПР9

- `data/podcast_planner.sqlite` — исходная база ПР7, хранится как источник переноса;
- `db.sqlite3` — целевая база Django ORM, локальная и исключена из Git.

SQL-слой ПР7 (`sql/`, `db/repository.py`) сохранён как предыдущая реализация, но Django views ПР9 его не используют.

## Первый запуск ПР9

```bash
pip install -r requirements.txt
python manage.py check
python manage.py makemigrations
python manage.py migrate
python db/inspect_source_db.py
python db/import_sqlite_to_orm.py
python manage.py showmigrations
python manage.py runserver
```

Импорт можно запускать повторно: используется `update_or_create()` с сохранением исходных ID.

## Проверка данных в Django shell

```bash
python manage.py shell
```

```python
from authors_web.models import User
from topics_web.models import Topic
from podcasts_web.models import Podcast
from episodes_web.models import Episode

User.objects.count()
Topic.objects.count()
Podcast.objects.count()
Episode.objects.count()
Episode.objects.select_related("podcast", "topic", "author").first()
```

Ожидаемое количество после импорта исходной базы ПР7:

```text
users: 6
topics: 15
podcasts: 10
episodes: 67
```

## Реализованные возможности ORM

- `all()`, `filter()`, `exclude()`, `get()`, `create()`;
- фильтрация по связанным полям;
- `Q()` для поиска по нескольким полям;
- `order_by()` с allow-list допустимых вариантов;
- `select_related()`;
- обратные связи `related_name`;
- `F()`, `values()`, `annotate()`, `aggregate()`, `Count()`;
- `get_object_or_404()`;
- срез QuerySet;
- `Paginator`;
- сохранение GET-параметров при переключении страниц.

Подробный список расположен в `ORM_QUERIES_PR9.md`.

## Страницы

- `/` — ORM-дашборд;
- `/podcasts/` — список и создание подкастов через ORM;
- `/podcasts/<id>/` — подкаст и обратная связь `podcast.episodes`;
- `/episodes/` — поиск, фильтры, сортировка, `values/annotate`, пагинация;
- `/episodes/<id>/` — `select_related()` и `get_object_or_404()`;
- `/statistics/` — `aggregate()` и `annotate()`;
- `/topics/`, `/authors/` — CRUD через ORM.

## Авторизация

```text
admin / admin123
anna / anna123
ivan / ivan123
maria / maria123
alex / alex123
elena / elena123
```

## Проверки

```bash
python manage.py check
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv,.venv
```

## Git ПР9

Все коммиты ПР9 начинаются с `PR9:`.

```bash
git add .
git commit -m "PR9: migrate data layer to Django ORM"
git push origin master
```
