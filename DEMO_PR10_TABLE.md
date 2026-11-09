# ПР10 — защита по таблице, 30 пунктов

Формат: **файл → Ctrl+F → строки → что показать → как реализовано → зачем**.  
Номера строк ориентировочные: если после правок они сдвинутся, ищи по тексту через `Ctrl+F`.

## Перед защитой

```bash
python manage.py migrate
python manage.py create_demo_superuser
python manage.py check
pytest -v
python manage.py runserver
```

Открыть заранее в браузере:

```text
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/episodes/
http://127.0.0.1:8000/statistics/
http://127.0.0.1:8000/podcasts/
```

Django Admin: `admin / admin123`.

---

## 1. Настройка Django Admin

**Файлы:** `authors_web/admin.py`, `topics_web/admin.py`, `podcasts_web/admin.py`, `episodes_web/admin.py`.  
**Ctrl+F:** `@admin.register`, `list_display`, `search_fields`, `list_filter`, `ordering`.  
**Строки:** `authors_web/admin.py` 6–20; `topics_web/admin.py` 6–12; `podcasts_web/admin.py` 15–28; `episodes_web/admin.py` 6–20.  
**Показать:** `/admin/` → Пользователи, Темы, Подкасты, Выпуски; в Выпусках поиск и фильтр по статусу.  
**Как:** `ModelAdmin` задаёт столбцы, поиск, фильтры, сортировку и размер страницы.  
**Зачем:** управлять ORM-моделями без отдельных страниц редактирования.

## 2. Связанные объекты в Admin

**Файл:** `podcasts_web/admin.py`.  
**Ctrl+F:** `class EpisodeInline`, `inlines =`.  
**Строки:** 8–12 и 26.  
**Показать:** Admin → Подкасты → открыть подкаст → внизу связанные выпуски.  
**Как:** `Episode` связан с `Podcast` через `ForeignKey`, а `TabularInline` показывает связанные записи.  
**Зачем:** редактировать связанные выпуски прямо из карточки подкаста.

## 3. Изменение модели и миграции

**Файлы:** `podcasts_web/models.py`, `podcasts_web/migrations/0002_podcast_slug.py`, `0003_podcast_title_length.py`.  
**Ctrl+F:** `SlugField`, `GeneratedField`, `migrations.AddField`.  
**Строки:** модель 13–25; миграция `0002` 20–33; `0003` 7–21.  
**Показать:**

```bash
python manage.py showmigrations
python manage.py makemigrations --check
```

**Как:** изменение модели фиксируется отдельным файлом миграции. `makemigrations` создаёт описание изменения, `migrate` применяет его к БД.  
**Зачем:** структура базы изменяется воспроизводимо и хранится в Git.

## 4. Преобразование существующих данных

**Файл:** `podcasts_web/migrations/0002_podcast_slug.py`.  
**Ctrl+F:** `fill_slugs`, `RunPython`.  
**Строки:** 5–17 и 28.  
**Показать:** функция проходит по существующим Podcast и создаёт slug до включения `unique=True`.  
**Как:** `RunPython(fill_slugs, ...)` — миграция данных, а не только схемы.  
**Зачем:** старые записи должны получить корректные значения нового поля до установки ограничения уникальности.

> В Podcast Planner статусы выпусков существовали ещё до ПР10, поэтому аналог преобразования старых данных показывается на реальной миграции slug.

## 5. Работа с моделями через Django Shell

**Команда:**

```bash
python manage.py shell
```

```python
from authors_web.models import User
from topics_web.models import Topic
from podcasts_web.models import Podcast
from episodes_web.models import Episode

Episode.objects.all()[:3]
e = Episode.objects.first()
e.status
```

**Как:** `objects` — менеджер ORM, возвращает `QuerySet`.  
**Зачем:** проверять модели и запросы без браузера.

## 6. Create / Update / Delete через ORM

**Shell:**

```python
from topics_web.models import Topic
x = Topic.objects.create(name="PR10 TEST")
x.name = "PR10 TEST 2"
x.save()
x.delete()
```

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `Episode.objects.create`.  
**Строки:** 64–79.  
**Как:** `create()` создаёт запись, `save()` сохраняет изменение, `delete()` удаляет.  
**Зачем:** CRUD выполняется через ORM, без ручного SQL.

## 7. QuerySet и несколько условий

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `release_date__gte`, `release_date__lte`.  
**Строки:** 92–107.  
**Показать:**

```text
/episodes/?status=published&date_from=2026-09-01&date_to=2026-12-31
```

**Как:** к одному QuerySet последовательно добавляются `filter(status=...)`, `filter(release_date__gte=...)`, `filter(release_date__lte=...)`.  
**Зачем:** строка остаётся в выборке только если выполняются все активные условия.

## 8. Фильтрация по связанным полям

**Файл:** `episodes_web/models.py`.  
**Ctrl+F:** `podcast__title__icontains`.  
**Строки:** 29–37.  
**Показать:** также `topic__name__icontains` и `author__name__icontains`.  
**Как:** двойное подчёркивание проходит по `ForeignKey` к полю связанной модели.  
**Зачем:** искать выпуск сразу по названию подкаста, теме или автору.

## 9. Собственный QuerySet

**Файл:** `episodes_web/models.py`.  
**Ctrl+F:** `class EpisodeQuerySet`.  
**Строки:** 11–37 и 76.  
**Показать:** `published()`, `in_progress()`, `ready()`, `for_date()`, `by_author()`, `search()`; `objects = EpisodeQuerySet.as_manager()`.  
**Shell:**

```python
Episode.objects.published()
Episode.objects.ready()
```

**Зачем:** повторяемые условия находятся в одном месте и не дублируются во views.

## 10. Обработка пользовательского ввода

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `request.GET.get`, `_parse_date`.  
**Строки:** 24–30 и 82–90.  
**Показать:** `/episodes/?date_from=abc`.  
**Как:** дата преобразуется через `date.fromisoformat`, `ValueError` превращается в сообщение `filter_error`.  
**Зачем:** неправильный GET-параметр не вызывает traceback.

## 11. Динамическая сортировка

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `SORT_FIELDS`, `order_by`.  
**Строки:** 16–21 и 106–107.  
**Показать:** `?sort=date_desc`, затем `?sort=title`.  
**Как:** пользовательское значение переводится через разрешённый словарь в безопасное поле ORM.  
**Зачем:** нельзя передавать произвольный ввод напрямую в `order_by()`.

## 12. values()

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `.values(`.  
**Строки:** 109–128.  
**Показать:** выбираются только `id`, `title`, названия связанных сущностей, статус и дата.  
**Как:** `values()` возвращает словари, а не полные объекты Episode.  
**Зачем:** не получать поля, которые таблице HTML не нужны.

## 13. annotate() и F()

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `queryset.annotate`.  
**Строки:** 110–116.  
**Показать:**

```python
podcast_title=F("podcast__title")
topic_name=F("topic__name")
author_name=F("author__name")
```

**Как:** значения из связанных таблиц получают собственные имена в результате QuerySet.  
**Зачем:** шаблон получает готовые поля одним ORM-запросом.

## 14. get_object_or_404()

**Файлы:** `episodes_web/views.py`, `podcasts_web/views.py`.  
**Ctrl+F:** `get_object_or_404`.  
**Строки:** Episode 162–165; Podcast 60–63 и 86–89.  
**Показать:** `/episodes/999999/` или несуществующий slug.  
**Как:** если объект отсутствует, Django возвращает HTTP 404.  
**Зачем:** нет необработанного `DoesNotExist`.

## 15. slug + get_absolute_url()

**Файлы:** `podcasts_web/models.py`, `podcasts_web/urls.py`, `podcast_card.html`.  
**Ctrl+F:** `SlugField`, `get_absolute_url`, `<slug:slug>`.  
**Строки:** модель 13–17 и 49–50; URL строка 9.  
**Показать:** карточка подкаста → ссылка вида `/podcasts/slug/.../`; в Admin работает «Посмотреть на сайте».  
**Как:** `get_absolute_url()` вызывает `reverse("podcasts_web:detail_slug", kwargs={...})`.  
**Зачем:** адрес формируется по имени маршрута, а не вручную.

## 16. GeneratedField

**Файлы:** `podcasts_web/models.py`, `podcasts_web/migrations/0003_podcast_title_length.py`.  
**Ctrl+F:** `title_length = models.GeneratedField`, `Length("title")`, `db_persist=True`.  
**Строки:** модель 20–25; миграция 7–21.  
**Shell:**

```python
p = Podcast.objects.first()
p.title_length
p.title = "Новое длинное название"
p.save()
p.refresh_from_db()
p.title_length
```

**Как:** база вычисляет длину `title` через `Length("title")`; значение хранится как generated column.  
**Зачем:** вычисляемое поле не синхронизируется вручную.

## 17. aggregate() + Count() + Q()

**Файл:** `homepage/views.py`.  
**Ctrl+F:** `episodes.aggregate`.  
**Строки:** 95–101; похожий запрос есть 59–65.  
**Показать:** `/statistics/`.  
**Как:** `Count("id")` считает все выпуски, `filter=Q(status=...)` — только опубликованные.  
**Зачем:** несколько сводных показателей рассчитываются средствами ORM.

## 18. Групповая статистика

**Файл:** `homepage/views.py`.  
**Ctrl+F:** `episodes.values("status")`.  
**Строки:** 107–113; статистика по подкастам 127–136.  
**Как:** `values("status").annotate(count=Count("id"))` создаёт группы по статусу.  
**Зачем:** получить количество выпусков в каждой категории.

## 19. select_related()

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `select_related("podcast", "topic", "author")`.  
**Строки:** 92–94 и 162–164.  
**Показать:** `/episodes/1/` → Debug Toolbar → SQL.  
**Как:** связанные `ForeignKey`-объекты загружаются вместе с Episode.  
**Зачем:** уменьшает N+1 запросов при обращении к связанным объектам.

## 20. Django Debug Toolbar

**Файлы:** `podcast_planner/settings.py`, `podcast_planner/urls.py`.  
**Ctrl+F:** `debug_toolbar`, `__debug__`.  
**Строки:** settings 23, 33, 87; urls 9.  
**Показать:** `/episodes/` → панель справа → SQL.  
**Как:** middleware перехватывает запрос и показывает выполненные SQL-запросы.  
**Зачем:** видно COUNT пагинации, SELECT списка и возможные лишние запросы.

## 21. Фильтрация + сортировка + пагинация

**Файлы:** `episodes_web/views.py`, `episode_list.html`.  
**Ctrl+F:** `Paginator`, `query_params`, `page_obj`.  
**Строки views:** 130–141.  
**Показать:** задать фильтр + сортировку → перейти на страницу 2.  
**Как:** `Paginator(rows, 10)` делит результат, а `params.urlencode()` сохраняет остальные GET-параметры.  
**Зачем:** пользователь не теряет выбранные фильтры при переходе между страницами.

## 22. Состояние выпуска на выбранную дату — адаптация предметной области

**Файл:** `episodes_web/models.py`.  
**Ctrl+F:** `for_date`, `published`, `in_progress`.  
**Строки:** 14–24.  
**Shell:**

```python
from datetime import date
Episode.objects.for_date(date(2026, 10, 1))
Episode.objects.in_progress().for_date(date(2026, 10, 1))
```

**Как:** для Podcast Planner вместо «свободных помещений» проверяется план выпусков на дату с учётом статуса.  
**Зачем:** демонстрируется та же идея предметного ограничения по дате и состоянию, адаптированная под подкасты.

## 23. Контекстный процессор

**Файлы:** `homepage/context_processors.py`, `podcast_planner/settings.py`, `templates/base.html`.  
**Ctrl+F:** `def project_context`, `homepage.context_processors.project_context`.  
**Строки:** context processor 20–26; settings 50–56.  
**Показать:** footer на нескольких страницах: общее число подкастов и выпусков.  
**Как:** processor возвращает `site_name`, `global_podcast_count`, `global_episode_count` для всех шаблонов.  
**Зачем:** общие данные не дублируются в каждом view.

## 24. TextChoices

**Файл:** `episodes_web/models.py`.  
**Ctrl+F:** `class Status(models.TextChoices)`.  
**Строки:** 41–46 и поле status 68–73.  
**Показать:** Admin → Выпуск → поле статуса; в коде `Episode.Status.PUBLISHED`.  
**Как:** в БД хранится строковый код, пользователю показывается человекочитаемое название.  
**Зачем:** нет случайных строк статусов по всему проекту.

## 25. Связанные данные без лишних запросов

**Файл:** `episodes_web/views.py`.  
**Ctrl+F:** `annotate(` и `.values(`.  
**Строки:** 110–128.  
**Показать:** Debug Toolbar → SQL списка.  
**Как:** `F()` + `values()` получают нужные связанные значения одним запросом.  
**Зачем:** здесь отдельный `select_related()` для итоговых словарей не требуется.

## 26. Пересчёт вычисляемого и связанного значения

**Файлы:** `podcasts_web/models.py`, `episodes_web/models.py`.  
**Ctrl+F:** `title_length`, `ForeignKey`.  
**Показать:** Admin → изменить название тестового подкаста → сохранить → `title_length` изменится; у выпуска можно изменить тему/автора и снова открыть запись.  
**Как:** `title` хранится напрямую, `title_length` вычисляет БД, ForeignKey хранит ссылку на другую строку.  
**Зачем:** показать разницу обычного, вычисляемого и связанного значения.

## 27. Именованные маршруты и ссылки

**Файлы:** `podcasts_web/urls.py`, `podcasts_web/models.py`, `podcast_card.html`.  
**Ctrl+F:** `name="detail_slug"`, `reverse(`, `get_absolute_url`.  
**Строки:** urls 9; model 49–50.  
**Показать:** список подкастов → карточка → подробная страница → назад.  
**Как:** ссылка формируется методом модели через имя маршрута.  
**Зачем:** путь можно изменить централизованно, не переписывая шаблоны.

## 28. Корректность ORM-запроса и безопасная ошибка

**Файлы:** `episodes_web/views.py`, `podcasts_web/views.py`, `tests/test_pr10.py`.  
**Ctrl+F:** `get_object_or_404`, `test_missing_podcast_slug_returns_404`.  
**Строки теста:** 52–56.  
**Показать:** несуществующий объект/slug или тест.  
**Как:** ожидаемая ошибка отсутствия объекта превращается в контролируемый HTTP-ответ.  
**Зачем:** рабочую БД намеренно ломать не требуется.

## 29. Проверка моделей и миграций

**Терминал:**

```bash
python manage.py makemigrations --check
python manage.py check
python manage.py showmigrations
```

**Как:** первая команда ищет изменения моделей без миграций; `check` проверяет конфигурацию; `showmigrations` показывает применённые миграции.  
**Зачем:** доказать согласованность кода моделей и структуры БД.

## 30. Автоматизированный тест

**Файл:** `tests/test_pr10.py`.  
**Ctrl+F:** `test_custom_queryset_and_relations`, `test_podcast_slug_and_absolute_url`, `test_generated_title_length`.  
**Строки:** 33–68.  
**Команда:**

```bash
pytest -v
```

**Как:** тесты автоматически проверяют QuerySet, связи, slug/get_absolute_url и GeneratedField.  
**Зачем:** подтверждение сценария не зависит только от ручного кликанья в браузере.

---

# Что открыть заранее в PyCharm

1. `episodes_web/models.py`
2. `episodes_web/views.py`
3. `episodes_web/admin.py`
4. `podcasts_web/models.py`
5. `podcasts_web/admin.py`
6. `podcasts_web/migrations/0002_podcast_slug.py`
7. `podcasts_web/migrations/0003_podcast_title_length.py`
8. `homepage/context_processors.py`
9. `homepage/views.py`
10. `podcast_planner/settings.py`
11. `tests/test_pr10.py`

# Быстрые команды Django Shell

```python
from authors_web.models import User
from topics_web.models import Topic
from podcasts_web.models import Podcast
from episodes_web.models import Episode

Episode.objects.published().count()
Episode.objects.ready().count()
Episode.objects.select_related("podcast", "topic", "author").first()
Podcast.objects.first().get_absolute_url()
p = Podcast.objects.first(); (p.title, p.title_length)
```

# Git

```bash
git status
git add .
git commit -m "PR10: configure Django Admin and inspect ORM queries"
git push origin master
```
