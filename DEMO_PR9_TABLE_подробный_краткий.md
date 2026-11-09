# ПР9 — защита по таблице: где что искать и что говорить

> **Важно:** номера строк указаны для текущей версии проекта. Если после правок они сдвинутся — ориентируйся по `Ctrl+F` и строке поиска, указанной в каждом пункте.

## Что открыть заранее

В PyCharm держи вкладки:

- `authors_web/models.py`
- `topics_web/models.py`
- `podcasts_web/models.py`
- `episodes_web/models.py`
- `episodes_web/views.py`
- `podcasts_web/views.py`
- `homepage/views.py`
- `homepage/auth.py`
- `episodes_web/templates/episodes_web/episode_list.html`
- `episodes_web/templates/episodes_web/episode_detail.html`
- `db/import_sqlite_to_orm.py`

В терминале заранее можно открыть Django shell:

```bash
python manage.py shell
```

---

## 1. Описание модели данных

**Файл:** `episodes_web/models.py`  
**Искать:** `class Episode` — строки примерно **10–65**.

**Показать:**

```python
status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.IDEA,
)
release_date = models.DateField(...)
```

**Как реализовано:** `Episode` — Django-модель; поля модели становятся столбцами таблицы.

**Зачем:** `choices` ограничивает допустимые статусы, `default` задаёт значение по умолчанию. `blank` относится к проверке формы, `null` — к хранению `NULL` в БД. Здесь они не нужны, потому что основные поля обязательные.

---

## 2. Связи ForeignKey

**Файл:** `episodes_web/models.py`  
**Искать:** `models.ForeignKey` — строки **18–40**.

**Показать:**

```python
podcast = models.ForeignKey(
    Podcast,
    on_delete=models.PROTECT,
    related_name="episodes",
)
```

То же для `topic` и `author`.

**Как реализовано:** у выпуска три связи «многие к одному».

**Зачем:** много выпусков могут относиться к одному подкасту, теме и автору. `PROTECT` не даёт удалить связанную запись, пока на неё ссылаются выпуски. `related_name="episodes"` даёт обратный доступ.

---

## 3. Прямая и обратная связь

**Файлы:** `episodes_web/models.py`, `podcasts_web/views.py`.  
**Искать:** `related_name="episodes"`, затем `podcast.episodes` — `podcasts_web/views.py`, строки **68–71**.

**Показать:**

```python
podcast.episodes.select_related("topic", "author")
```

В shell:

```python
episode = Episode.objects.first()
episode.podcast
podcast = Podcast.objects.first()
podcast.episodes.all()
```

**Как реализовано:** `episode.podcast` — прямая связь, `podcast.episodes.all()` — обратная.

**Зачем:** `related_name` делает обратное обращение понятным и коротким.

---

## 4. Миграции

**Файлы:**

- `authors_web/migrations/0001_initial.py`
- `topics_web/migrations/0001_initial.py`
- `podcasts_web/migrations/0001_initial.py`
- `episodes_web/migrations/0001_initial.py`

**Искать:** `migrations.CreateModel`.

**Показать команды:**

```bash
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate
```

**Как реализовано:** миграции создают таблицы ORM-моделей и ForeignKey.

**Зачем:** изменение Python-модели само по себе не изменяет структуру БД; `makemigrations` создаёт описание изменений, `migrate` применяет их.

---

## 5. Создание объекта через ORM

**Файл:** `episodes_web/views.py`  
**Искать:** `Episode.objects.create` — строки **72–79**.

```python
Episode.objects.create(
    podcast=podcast,
    title=title,
    topic=topic,
    author=author,
    status=status,
    release_date=release_date,
)
```

**Как реализовано:** данные формы POST проверяются, затем ORM создаёт запись.

**Зачем:** `objects.create()` сразу создаёт и сохраняет объект в БД.

---

## 6. Изменение объекта через ORM

**Файл:** `episodes_web/models.py`  
**Искать:** `def change_status` — строки **55–59**.

```python
self.status = status
self.save(update_fields=["status"])
```

**Как реализовано:** меняется атрибут объекта и вызывается `save()`.

**Зачем:** присваивание меняет объект только в памяти; `save()` фиксирует изменение в БД. `update_fields` обновляет только нужное поле.

---

## 7. Удаление объекта

**Файл:** `episodes_web/views.py`  
**Искать:** `episode.delete()` — строки **184–186**.

```python
elif action == "delete":
    episode.delete()
```

**Как реализовано:** удаляется ORM-объект выпуска.

**Зачем:** `delete()` удаляет соответствующую запись. Для связанных подкаста/темы/автора используется `PROTECT`, поэтому их случайное удаление при существующих выпусках запрещено.

---

## 8. QuerySet и filter()

**Файл:** `episodes_web/views.py`  
**Искать:** `queryset = Episode.objects` — строки **92–110**.

```python
queryset = Episode.objects.select_related(...)
queryset = queryset.filter(status=status)
```

**Как реализовано:** сначала создаётся QuerySet, затем к нему последовательно добавляются условия.

**Зачем:** QuerySet ленивый — SQL фактически выполняется, когда данные реально понадобятся.

---

## 9. Фильтрация по полю связанной модели

**Файл:** `episodes_web/views.py`  
**Искать:** `podcast__title__icontains` — строки **98–104**.

```python
Q(podcast__title__icontains=query)
| Q(topic__name__icontains=query)
| Q(author__name__icontains=query)
```

**Как реализовано:** двойное подчёркивание `__` позволяет пройти по ForeignKey к полю связанной модели.

**Зачем:** можно искать выпуск не только по его названию, но и по подкасту, теме или автору.

---

## 10. Несколько условий фильтрации

**Файл:** `episodes_web/views.py`  
**Искать:** `if query:`, `if status`, `date_from`, `date_to` — строки **98–110**.

**Показать:** одновременно могут применяться:

- текстовый поиск;
- статус;
- дата от;
- дата до;
- ограничение по автору.

**Как реализовано:** каждый `.filter()` добавляет ещё одно условие к тому же QuerySet.

**Зачем:** итоговая выборка удовлетворяет всем активным фильтрам.

---

## 11. Проверка пользовательского ввода

**Файл:** `episodes_web/views.py`  
**Искать:** `def _parse_date` — строки **24–30** и `request.GET.get` — строки **82–90**.

```python
try:
    return date.fromisoformat(value), None
except ValueError:
    return None, f"Некорректная дата: {value}"
```

**Как реализовано:** строки из GET преобразуются в `date`, ошибка перехватывается.

**Зачем:** неправильная дата не должна приводить к 500.

**Проверка:** `/episodes/?date_from=abc`.

---

## 12. Сортировка order_by()

**Файл:** `episodes_web/views.py`  
**Искать:** `SORT_FIELDS` — строки **16–21**, затем `order_by` — строки **112–113**.

```python
order_field = SORT_FIELDS.get(sort_value, "release_date")
queryset = queryset.order_by(order_field, "pk")
```

**Как реализовано:** поле сортировки выбирается из разрешённого словаря.

**Зачем:** `-release_date` означает обратный порядок; второе поле `pk` делает порядок стабильным.

---

## 13. Безопасный выбор поля сортировки

**Файл:** `episodes_web/views.py`  
**Искать:** `SORT_FIELDS`.

```python
SORT_FIELDS = {
    "date": "release_date",
    "date_desc": "-release_date",
    "title": "title",
    "podcast": "podcast__title",
}
```

**Как реализовано:** пользователь передаёт не имя поля БД, а безопасный ключ `date`, `title` и т.д.

**Зачем:** нельзя делать `order_by(request.GET["sort"])` без проверки. Неизвестное значение заменяется на `release_date`.

---

## 14. values()

**Файл:** `episodes_web/views.py`  
**Искать:** `.values(` — строки **123–133**.

```python
.values(
    "id",
    "title",
    "podcast_title",
    "topic_name",
    "author_name",
    ...
)
```

**Как реализовано:** ORM возвращает словари только с перечисленными полями.

**Зачем:** для списка не требуется загружать все поля полноценных объектов.

---

## 15. annotate() и F()

**Файл:** `episodes_web/views.py`  
**Искать:** `queryset.annotate` — строки **116–122**.

```python
podcast_title=F("podcast__title"),
topic_name=F("topic__name"),
author_name=F("author__name"),
```

**Как реализовано:** к каждой строке QuerySet добавляются вычисляемые поля из связанных моделей.

**Зачем:** затем их удобно передать в `.values()` и использовать в шаблоне как `episode.podcast_title`.

---

## 16. Получение объекта и 404

**Файл:** `episodes_web/views.py`  
**Искать:** `get_object_or_404` — строки **168–171**.

```python
episode = get_object_or_404(
    Episode.objects.select_related(...),
    pk=episode_id,
)
```

**Как реализовано:** если объекта нет, Django автоматически возвращает HTTP 404.

**Зачем:** не возникает необработанного `DoesNotExist`.

**Проверка:** `/episodes/999999/`.

---

## 17. COUNT / aggregate()

**Файл:** `homepage/views.py`  
**Искать:** `episodes.aggregate` — строки **59–65** или **97–103**.

```python
totals = episodes.aggregate(
    episode_count=Count("id"),
    published_count=Count(
        "id",
        filter=Q(status=Episode.Status.PUBLISHED),
    ),
)
```

**Как реализовано:** агрегирование возвращает один словарь с итоговыми значениями.

**Зачем:** считаются все выпуски и отдельно опубликованные без загрузки всех объектов в Python.

---

## 18. Статистика по группам

**Файл:** `homepage/views.py`  
**Искать:** `values("status")` — строки **109–115** и `podcasts.annotate` — строки **129–139**.

```python
episodes.values("status").annotate(count=Count("id"))
```

и

```python
podcasts.annotate(
    episodes_count=Count("episodes"),
    published_count=Count(...),
)
```

**Как реализовано:** `values()` задаёт группу, `annotate()` считает показатель для каждой группы/объекта.

**Зачем:** формируется статистика по статусам и подкастам средствами БД.

---

## 19. select_related()

**Файл:** `episodes_web/views.py`  
**Искать:** `Episode.objects.select_related` — строки **92–94** и **168–170**.

```python
Episode.objects.select_related("podcast", "topic", "author")
```

**Как реализовано:** связанные ForeignKey-объекты подгружаются одним SQL-запросом.

**Зачем:** при последующем `episode.podcast`, `episode.topic`, `episode.author` не нужны отдельные запросы для каждой связи.

---

## 20. Получение только необходимых данных

**Файл:** `episodes_web/views.py`  
**Искать:** `rows = (` — строки **115–134**.

**Показать:** связка

```python
annotate(...).values(...)
```

**Как реализовано:** сначала создаются удобные имена связанных полей, потом выбирается только набор, нужный таблице HTML.

**Зачем:** уменьшается объём данных, которые получает приложение.

---

## 21. ORM → context → шаблон

**Файл 1:** `episodes_web/views.py`  
**Искать:** `"episodes": page_obj.object_list` — строки **141–162**.

```python
"episodes": page_obj.object_list,
```

**Файл 2:** `episodes_web/templates/episodes_web/episode_list.html`  
**Искать:** `{% for episode in episodes %}` — примерно строка **35**.

**Как реализовано:** результат ORM кладётся в context под ключом `episodes`; шаблон перебирает эту переменную.

**Зачем:** view отвечает за данные, template — за HTML. Если имя изменить только в одном месте, список перестанет отображаться.

---

## 22. Paginator

**Файл:** `episodes_web/views.py`  
**Искать:** `Paginator(` — строки **136–137**.

```python
paginator = Paginator(rows, 10)
page_obj = paginator.get_page(request.GET.get("page", 1))
```

**Как реализовано:** на одну страницу выдаётся 10 записей.

**Зачем:** большой список не выводится целиком. Если поменять `10` на `5`, страниц станет больше.

---

## 23. Навигация пагинации

**Файл:** `episodes_web/templates/episodes_web/episode_list.html`  
**Искать:** `page_obj.has_previous` — строки примерно **39–44**.

```django
{% if page_obj.has_previous %}
...
{% endif %}

{% if page_obj.has_next %}
...
{% endif %}
```

**Как реализовано:** ссылки «назад/вперёд» появляются только когда соответствующая страница существует.

**Зачем:** на первой странице нет перехода назад, на последней — вперёд.

---

## 24. Сохранение фильтров при пагинации

**Файл 1:** `episodes_web/views.py`  
**Искать:** `params = request.GET.copy()` — строки **138–139**, затем `query_params` — строка **147**.

```python
params = request.GET.copy()
params.pop("page", None)
"query_params": params.urlencode(),
```

**Файл 2:** `episode_list.html`  
**Искать:** `query_params` — строки примерно **41–43**.

**Как реализовано:** текущие GET-параметры сохраняются, меняется только `page`.

**Зачем:** при переходе на страницу 2 не сбрасываются поиск, статус, даты и сортировка.

---

## 25. Фильтрация + сортировка + пагинация вместе

**Файл:** `episodes_web/views.py`  
**Искать:** блок от `request.GET.get` до `Paginator` — строки **82–139**.

**Как реализовано, порядок:**

1. получаем GET;
2. проверяем даты;
3. фильтруем QuerySet;
4. сортируем;
5. `annotate/values`;
6. пагинация.

**Зачем:** сначала определяется состав и порядок записей, затем только нужная страница.

**Проверка:**

```text
/episodes/?status=published&sort=date_desc&page=2
```

---

## 26. Объекты без связанных записей

**Файл:** `homepage/views.py`  
**Искать:** `podcasts.annotate` — строки **129–139**.

```python
podcasts.annotate(
    episodes_count=Count("episodes"),
    ...
)
```

**Как реализовано:** Django агрегирует обратную связь `episodes`; подкаст без выпусков получает `episodes_count = 0` и не обязан исчезать из результата.

**Зачем:** статистика должна показывать и подкасты, у которых пока нет выпусков.

---

## 27. exclude()

**Файл:** `homepage/views.py`  
**Искать:** `episodes.exclude` — строки **70–72**.

```python
episodes.exclude(
    status=Episode.Status.PUBLISHED
).count()
```

**Как реализовано:** из выборки исключаются опубликованные выпуски.

**Зачем:** считается число выпусков, которые ещё находятся в работе.

---

## 28. Ограничение количества записей срезом

**Файл:** `homepage/views.py`  
**Искать:** `[:5]` — строки **79–82**.

```python
episodes.select_related(...)
.order_by("release_date", "pk")[:5]
```

**Как реализовано:** QuerySet ограничивается пятью строками.

**Зачем:** на главной нужны только 5 ближайших выпусков, а не весь список.

---

## 29. Получение одной записи через get()

**Файл:** `homepage/auth.py`  
**Искать:** `User.objects.get` — строки **18–21**.

```python
try:
    return User.objects.get(pk=user_id)
except User.DoesNotExist:
    return None
```

**Как реализовано:** `get()` ожидает ровно одну запись; отсутствие обрабатывается исключением.

**Зачем:** по ID из сессии нужно получить одного текущего пользователя. Для страниц объектов удобнее `get_object_or_404()`.

---

## 30. ORM + связанные модели во view

**Файл:** `episodes_web/views.py`  
**Искать:** `def episode_detail` — строки **165–193**.

**Показать цепочку:**

```python
get_object_or_404(
    Episode.objects.select_related("podcast", "topic", "author"),
    pk=episode_id,
)
```

затем:

```python
return render(
    request,
    "episodes_web/episode_detail.html",
    {"episode": episode, ...},
)
```

**Шаблон:** `episodes_web/templates/episodes_web/episode_detail.html`  
**Искать:** `episode.podcast.title`, `episode.author.name`, `episode.topic.name` — строки примерно **8–10**.

**Как реализовано:** URL передаёт ID → view получает Episode через ORM вместе со связями → объект идёт в context → шаблон выводит атрибуты.

**Зачем:** это полный путь данных ПР9 без ручного SQL:

```text
URL → view → Django ORM → SQLite → объект Episode → context → template → HTML
```

---

# Отдельно показать перенос ПР7 → ПР9

Это не отдельный пункт таблицы 1–30, но преподаватель может спросить.

**Файл:** `db/import_sqlite_to_orm.py`  
**Искать:** `update_or_create` — строки **44–80**.

**Как реализовано:**

1. старая база `data/podcast_planner.sqlite` читается через `sqlite3`;
2. сначала переносятся `User` и `Topic`;
3. затем `Podcast`;
4. затем зависимые `Episode`;
5. записи создаются через `Model.objects.update_or_create()`.

**Почему:** ПР7 остаётся источником данных, но рабочая БД ПР9 управляется Django ORM и миграциями.

---

# Быстрый Django shell перед защитой

```python
from authors_web.models import User
from topics_web.models import Topic
from podcasts_web.models import Podcast
from episodes_web.models import Episode

print(User.objects.count())
print(Topic.objects.count())
print(Podcast.objects.count())
print(Episode.objects.count())

episode = Episode.objects.select_related(
    "podcast", "topic", "author"
).first()

print(episode)
print(episode.podcast)
print(episode.topic)
print(episode.author)
```

---

# Команды перед защитой

```bash
python manage.py check
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=venv,.venv
python manage.py runserver
```

# Что сказать в начале защиты

> «В ПР9 я перевела слой работы с данными с ручных SQL-запросов ПР7 на Django ORM. Структура страниц и пользовательские сценарии сохранены. Теперь представления работают с Django-моделями, QuerySet, ForeignKey, миграциями, фильтрацией, агрегированием, связанными объектами и пагинацией.»
