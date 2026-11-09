# Podcast Planner — ПР10

ПР10 продолжает ПР9. Данные приложения остаются на Django ORM; добавлены и проверены административная панель Django, повторно используемые QuerySet, slug-маршруты, контекстный процессор и Django Debug Toolbar.

## Основное

- `/admin/` — Django Admin;
- `User`, `Topic`, `Podcast`, `Episode` зарегистрированы через `ModelAdmin`;
- настроены `list_display`, `list_display_links`, `search_fields`, `list_filter`, `ordering`, `list_per_page`;
- для `Podcast` настроен inline выпусков;
- для `Episode` настроены поиск по связанным моделям, фильтры, `autocomplete_fields`, `list_select_related` и admin actions;
- `EpisodeQuerySet`: `published()`, `in_progress()`, `ready()`, `for_date()`, `by_author()`, `search()`;
- `Podcast.slug` + `get_absolute_url()`;
- `Podcast.title_length` — `GeneratedField`, вычисляемый базой из `title`;
- сохранены фильтрация, сортировка и пагинация ПР9;
- Django Debug Toolbar подключён по `/__debug__/` при `DEBUG=True`;
- общий контекст содержит название сайта и общие счётчики;
- добавлены автоматизированные тесты ПР10.

## Первый запуск после ПР9

```bash
pip install -r requirements.txt
python manage.py makemigrations --check
python manage.py migrate
python manage.py create_demo_superuser
python manage.py check
pytest -v
flake8 . --extend-exclude=venv,.venv
python manage.py runserver
```

Если целевая `db.sqlite3` создаётся с нуля, после миграций перенесите данные ПР7:

```bash
python db/import_sqlite_to_orm.py
```

## Доступ

Пользовательский интерфейс:

```text
admin / admin123
```

Django Admin `/admin/`:

```text
admin / admin123
```

Это разные учётные записи в разных моделях: пользователь Podcast Planner и Django superuser.

## Проверка Debug Toolbar

Откройте `/episodes/` или `/episodes/1/`. При `DEBUG=True` справа отображается панель Django Debug Toolbar. Во вкладке SQL можно увидеть ORM-запросы, включая запросы со связями.

## Git

```bash
git add .
git commit -m "PR10: configure Django Admin and inspect ORM queries"
git push origin master
```

## GeneratedField

В `Podcast` добавлено вычисляемое поле:

```python
title_length = models.GeneratedField(
    expression=Length("title"),
    output_field=models.IntegerField(),
    db_persist=True,
)
```

Значение хранится и пересчитывается базой данных. После изменения `title`,
`save()` и `refresh_from_db()` поле `title_length` получает новую длину.
