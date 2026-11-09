# ПР10 — пункты 5–6 для демонстрации

## Система планирования выпуска подкастов

### 5. Работа с моделями через Django Shell

**Что открыть заранее**

Файлы:

- `authors_web/models.py`
- `topics_web/models.py`
- `podcasts_web/models.py`
- `episodes_web/models.py`

**Что искать**

`authors_web/models.py`:

```python
class User(models.Model):
```

примерно строки **13–53**.

`topics_web/models.py`:

```python
class Topic(models.Model):
```

примерно строки **6–19**.

`podcasts_web/models.py`:

```python
class Podcast(models.Model):
```

примерно строки **11–58**.

`episodes_web/models.py`:

```python
class Episode(models.Model):
```

примерно строки **40–94**.

**Что показать**

В `Episode` показать связи:

```python
podcast = models.ForeignKey(...)
topic = models.ForeignKey(...)
author = models.ForeignKey(...)
```

И `on_delete=models.PROTECT`.

---

### Что ввести в Django Shell

Запуск:

```bash
python manage.py shell
```

Импорт моделей:

```python
from authors_web.models import User
from topics_web.models import Topic
from podcasts_web.models import Podcast
from episodes_web.models import Episode
```

Получить объекты:

```python
User.objects.all()[:3]
Topic.objects.all()[:3]
Podcast.objects.all()[:3]
Episode.objects.all()[:3]
```

Получить один выпуск:

```python
episode = Episode.objects.first()
```

Прочитать поле:

```python
print(episode.title)
```

Показать связанный объект:

```python
print(episode.podcast)
print(episode.topic)
print(episode.author)
```

Изменить поле **только в памяти**:

```python
old_title = episode.title
episode.title = "Временное название для демонстрации"
print(episode.title)
```

Показать, что в базе старое значение:

```python
print(Episode.objects.get(pk=episode.pk).title)
```

Теперь сохранить:

```python
episode.save()
```

Повторно получить запись:

```python
print(Episode.objects.get(pk=episode.pk).title)
```

Вернуть исходное значение:

```python
episode.title = old_title
episode.save()
```

**Как реализовано**

ORM-модель `Episode` представляет строку таблицы `episodes_web_episode`.
`objects.all()` возвращает QuerySet, `first()` получает объект, изменение атрибута меняет объект Python, а `save()` сохраняет изменение в базе.

**Что сказать**

> Изменение атрибута объекта сначала происходит только в памяти Python. Пока не вызван `save()`, значение в базе данных остаётся прежним. После `save()` ORM выполняет SQL UPDATE, и повторный запрос возвращает новое значение.

---

## 6. Создание, изменение и удаление записей средствами ORM

Для безопасной демонстрации используем тестовую тему, чтобы не менять реальные данные проекта.

**Файл:** `topics_web/models.py`

**Искать:**

```python
class Topic(models.Model):
```

строки примерно **6–19**.

Поле:

```python
name = models.CharField(
    max_length=200,
    unique=True,
)
```

---

### Что ввести в Django Shell

Если Shell уже открыт, повторно запускать не нужно.

Импорт:

```python
from topics_web.models import Topic
```

### 1. Создать объект

```python
test_topic = Topic.objects.create(
    name="Тестовая тема ПР10"
)
```

Проверить:

```python
print(test_topic.id)
print(test_topic.name)
```

Показать, что запись есть в базе:

```python
Topic.objects.filter(
    pk=test_topic.pk
).exists()
```

Результат:

```text
True
```

### 2. Изменить объект

```python
test_topic.name = "Изменённая тестовая тема ПР10"
test_topic.save()
```

Повторно получить из базы:

```python
Topic.objects.get(
    pk=test_topic.pk
).name
```

Результат:

```text
'Изменённая тестовая тема ПР10'
```

### 3. Удалить тестовый объект

Сохранить ID:

```python
test_id = test_topic.pk
```

Удалить:

```python
test_topic.delete()
```

Проверить:

```python
Topic.objects.filter(
    pk=test_id
).exists()
```

Результат:

```text
False
```

**Как реализовано**

- `objects.create()` выполняет создание записи;
- изменение поля + `save()` приводит к обновлению записи;
- `delete()` удаляет запись из базы.

**Что сказать**

> Django ORM преобразует эти операции в SQL: создание — в `INSERT`, сохранение изменения — в `UPDATE`, удаление — в `DELETE`.

---

### Как показать влияние связей и `on_delete`

**Файл:** `episodes_web/models.py`

**Искать:** `on_delete=models.PROTECT`

Примерно строки **48–67**:

```python
podcast = models.ForeignKey(
    Podcast,
    on_delete=models.PROTECT,
)

topic = models.ForeignKey(
    Topic,
    on_delete=models.PROTECT,
)

author = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
)
```

**Что сказать**

> `PROTECT` запрещает удалять подкаст, тему или автора, если на объект ссылаются существующие выпуски. Это защищает связанные данные от случайного удаления.

Если преподаватель просит показать это в Shell, можно взять тему, которая используется в выпусках:

```python
used_topic = Episode.objects.first().topic
used_topic.delete()
```

Django должен вызвать `ProtectedError`.

**Важно:** после демонстрации ничего исправлять не нужно — объект не удалится.

---

## Что показать в базе PyCharm

Открыть:

`View → Tool Windows → Database`

Если база ещё не подключена:

`Create data source → SQLite → выбрать db.sqlite3 → Test Connection → OK`

Раскрыть:

```text
db.sqlite3
→ main
→ tables
```

Показать таблицы:

```text
authors_web_user
topics_web_topic
podcasts_web_podcast
episodes_web_episode
```

Для пункта 5 открыть:

```text
episodes_web_episode
```

Для пункта 6 открыть:

```text
topics_web_topic
```

**Что сказать**

> Django-модель соответствует таблице SQLite. ORM позволяет создавать, получать, изменять и удалять строки таблицы через Python-объекты без ручного SQL.

---

## Очень коротко на защите

### Пункт 5

> Через Django Shell я получаю объекты моделей через `objects.all()` и `first()`. Изменение атрибута сначала меняет только объект в памяти. Только после `save()` ORM сохраняет изменение в базе.

### Пункт 6

> `objects.create()` создаёт запись, изменение поля и `save()` обновляют её, `delete()` удаляет. ORM преобразует эти действия в `INSERT`, `UPDATE` и `DELETE`. Для связанных моделей `on_delete=PROTECT` запрещает удаление объекта, если на него ссылаются выпуски.
