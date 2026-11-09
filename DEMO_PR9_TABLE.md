# ПР9 — защита по таблице (30 пунктов)

Открыть заранее: `authors_web/models.py`, `topics_web/models.py`, `podcasts_web/models.py`, `episodes_web/models.py`, `episodes_web/views.py`, `podcasts_web/views.py`, `homepage/views.py`, `db/import_sqlite_to_orm.py`, `episodes_web/templates/episodes_web/episode_list.html`, `ORM_QUERIES_PR9.md`.

1. **Описание модели** — показать поля `Episode` и параметры `default`, choices; объяснить `null/blank`.
2. **ForeignKey** — `Episode.podcast/topic/author`, `on_delete=PROTECT`, `related_name`.
3. **Прямая/обратная связь** — `episode.podcast`, `podcast.episodes.all()`.
4. **Миграции** — `makemigrations`, `showmigrations`, `migrate`; показать `0001_initial.py`.
5. **Create** — `Episode.objects.create(...)` в `episodes_web/views.py`.
6. **Update** — `Episode.change_status()` → `save(update_fields=["status"])`.
7. **Delete** — `episode.delete()` в detail view; объяснить влияние `PROTECT`.
8. **QuerySet + filter** — начало `episodes()` и последовательные `.filter()`.
9. **Связанное поле** — `podcast__title__icontains`, `topic__name__icontains`.
10. **Несколько условий** — query + status + date_from + date_to + author.
11. **Проверка ввода** — `_parse_date()`; в браузере задать `date_from=abc`.
12. **order_by** — `order_field = SORT_FIELDS.get(...)`; поменять `date`/`date_desc`.
13. **Allow-list сортировки** — словарь `SORT_FIELDS`; неизвестное значение не передаётся напрямую в `order_by()`.
14. **values()** — показать `.values(...)` списка выпусков.
15. **annotate + F** — `podcast_title=F("podcast__title")`, `topic_name`, `author_name`.
16. **404** — `get_object_or_404()` в `episode_detail()`; открыть `/episodes/999999/`.
17. **aggregate/count** — `homepage/views.py` → `aggregate(Count(...))`.
18. **Статистика** — `values("status").annotate(count=Count("id"))` и статистика подкастов.
19. **select_related** — detail view: `select_related("podcast", "topic", "author")`.
20. **Только нужные данные** — список выпусков: `annotate(...).values(...)`.
21. **Context → template** — `render(... {"episodes": page_obj.object_list})` и `{% for episode in episodes %}`.
22. **Paginator** — `Paginator(rows, 10)`; изменить 10 на 5.
23. **Навигация** — `page_obj.has_previous/has_next` в шаблоне.
24. **Сохранение GET** — `query_params = params.urlencode()` и ссылки пагинации.
25. **Фильтр + сортировка + пагинация** — `/episodes/?status=published&sort=date_desc&page=2`.
26. **Объекты без связей** — статистика подкастов через `Count("episodes")` сохраняет подкасты без выпусков; объяснить LEFT OUTER JOIN ORM.
27. **exclude()** — `episodes.exclude(status=Episode.Status.PUBLISHED)` на главной.
28. **Срез** — ближайшие выпуски `[:5]` на главной.
29. **get()** — `User.objects.get(pk=user_id)` в `homepage/auth.py`; сравнить с `get_object_or_404()`.
30. **ORM + связи во view** — пройти `episode_detail`: URL → view → ORM → related objects → context → template.

Команды перед защитой:

```bash
python manage.py check
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv,.venv
python manage.py runserver
```
