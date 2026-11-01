# ПР6 — демонстрация по таблице оценивания (25 пунктов)

Проект: «Система планирования выпусков подкастов».

## Что открыть заранее в PyCharm

Двойной Shift → ввести путь.

1. `podcast_planner/settings.py`
2. `podcast_planner/urls.py`
3. `manage.py`
4. `templates/base.html`
5. `templates/includes/navigation.html`
6. `homepage/views.py`
7. `homepage/templates/homepage/index.html`
8. `podcasts_web/urls.py`
9. `podcasts_web/views.py`
10. `podcasts_web/templates/podcasts_web/podcast_list.html`
11. `podcasts_web/templates/podcasts_web/podcast_detail.html`
12. `podcasts_web/templates/podcasts_web/includes/podcast_card.html`
13. `episodes_web/views.py`
14. `episodes_web/templates/episodes_web/episode_list.html`
15. `episodes_web/templates/episodes_web/episode_detail.html`
16. `episodes_web/templates/episodes_web/includes/episode_status.html`
17. `homepage/static/homepage/css/style.css`
18. `homepage/static/homepage/js/main.js`
19. `data/podcasts.json`
20. `storage.py`

## Открыть в браузере

После входа `admin / admin123`:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/podcasts/`
- `http://127.0.0.1:8000/podcasts/1/`
- `http://127.0.0.1:8000/podcasts/9999/`
- `http://127.0.0.1:8000/episodes/`
- `http://127.0.0.1:8000/episodes/1/`
- `http://127.0.0.1:8000/episodes/9999/`

## Выполнить заранее

```bash
python manage.py check
pytest -v
flake8 . --extend-exclude=venv,.venv
python manage.py findstatic homepage/img/logo.png
python manage.py runserver
```

---

## 1. Запуск и проверка проекта

Показать терминал.

Сказать:

«`python manage.py check` проверяет конфигурацию Django без запуска
сервера. `python manage.py runserver` запускает development-сервер
и начинает принимать HTTP-запросы».

---

## 2. Формирование главной страницы

Показать:

`homepage/views.py` → `index()`.

Там:

```python
return render(
    request,
    "homepage/index.html",
    context,
)
```

Затем открыть:

`homepage/templates/homepage/index.html`.

Сказать:

«Запрос `/` попадает в `index()`. View получает данные,
создаёт context и вызывает `render()`.
Django обрабатывает `homepage/index.html`,
тот наследует `base.html`, после чего готовый HTML возвращается
браузеру как HTTP-ответ».

---

## 3. Формирование списка подкастов

Показать:

`podcasts_web/views.py` → `podcasts()`.

Показать context:

```python
context = {
    "podcasts": podcasts_list,
    ...
}
```

Затем:

`podcast_list.html`:

```django
{% for podcast in podcasts %}
```

Сказать:

«View загружает объекты из JSON и передаёт список `podcasts`
через context. Цикл выполняется уже в шаблоне, а не в Python-коде».

---

## 4. Страница отдельного подкаста

Показать:

`podcasts_web/urls.py`:

```python
path(
    "<int:podcast_id>/",
    views.podcast_detail,
    name="detail",
)
```

`podcasts_web/views.py`:

```python
podcast = find_podcast_by_id(
    podcasts_list,
    podcast_id,
)
```

И `podcast_detail.html`:

```django
{{ podcast.title }}
{{ podcast.description }}
{{ podcast.author.name }}
```

Сказать:

«ID из URL Django передаёт в `podcast_id`.
View ищет объект функцией `find_podcast_by_id()`.
Объект передаётся в шаблон через context, где отображаются его
атрибуты».

---

## 5. Формирование списка выпусков

Показать:

`episodes_web/views.py` → `episodes()`.

Затем:

`episode_list.html`:

```django
{% for episode in episodes %}
```

и:

```django
{% include "episodes_web/includes/episode_status.html" %}
```

Сказать:

«Список выпусков передаётся в context.
Шаблон перебирает коллекцию циклом.
Для каждого выпуска повторяющийся HTML статуса подключается
отдельным include-шаблоном».

---

## 6. Страница отдельного выпуска

Показать:

`episode_detail()` и `episode_detail.html`.

Сказать:

«Нужный выпуск определяется по `episode_id`.
В шаблон передаётся объект `episode`.
Показываются название, подкаст, автор, тема, дата и статус.

Если ID отсутствует, `episode=None`, шаблон показывает ветку
ошибки, а `render()` возвращает HTTP 404».

Показать:

```python
status=404 if episode is None else 200
```

И открыть `/episodes/9999/`.

---

## 7. Переходы между страницами

Показать:

`templates/includes/navigation.html`.

Ссылки:

```django
{% url 'homepage:index' %}
{% url 'podcasts_web:podcasts' %}
{% url 'episodes_web:episodes' %}
```

Сказать:

«URL определены в `urls.py`, а шаблон обращается к ним по имени.
Адреса основных страниц не зашиваются вручную».

---

## 8. Базовый шаблон

Показать:

`templates/base.html`.

Сказать:

«`base.html` содержит общую структуру:
DOCTYPE, head, title, Bootstrap, собственный CSS, навигацию,
основной контейнер, footer и JavaScript.
Дублировать это на каждой странице не нужно».

---

## 9. Наследование шаблонов

Показать в `podcast_list.html`:

```django
{% extends "base.html" %}
```

Сказать:

«`extends` связывает дочерний шаблон с `base.html`.
Дочерний шаблон заполняет только объявленные блоки.
Если убрать `extends`, содержимое блоков не получит общий каркас
сайта».

---

## 10. Блоки шаблона

В `base.html`:

```django
{% block title %}
{% endblock %}

{% block content %}
{% endblock %}
```

В дочернем шаблоне показать переопределение.

Сказать:

«Чтобы изменить заголовок или содержимое конкретной страницы,
переопределяется соответствующий block. Общий каркас не меняется».

---

## 11. Передача контекста

Показать `podcasts()`:

```python
context = {
    "podcasts": podcasts_list,
    "authors": ...,
}
```

и:

```python
return render(
    request,
    "podcasts_web/podcast_list.html",
    context,
)
```

В шаблоне:

```django
{{ podcasts|length }}
{% for podcast in podcasts %}
```

Сказать:

«Имена ключей context становятся переменными Django Template
Language. Если изменить значение `podcasts` во view, шаблон получит
уже другое значение».

---

## 12. Вывод значений DTL

Показать:

```django
{{ podcast.title }}
{{ podcast.author.name }}
```

Сказать:

«Двойные фигурные скобки выводят данные из context и атрибуты
объектов. В отличие от ПР5, Python больше не собирает HTML-строку».

---

## 13. Циклы

Показать в `podcast_list.html`:

```django
{% for podcast in podcasts %}
```

Сказать:

«Коллекция `podcasts` перебирается шаблоном.
Количество карточек автоматически равно количеству объектов в
списке».

---

## 14. Условия

Показать в `episode_status.html`:

```django
{% if episode.status.value == "published" %}
...
{% elif ... %}
...
{% else %}
...
{% endif %}
```

Сказать:

«Условия меняют отображение в зависимости от состояния объекта.
Альтернативная ветка задаётся через `else` или `elif`».

---

## 15. Пустая коллекция

Показать:

```django
{% for podcast in podcasts %}
    ...
{% empty %}
    Подкасты не найдены.
{% endfor %}
```

Сказать:

«`empty` выполняется, если список пуст.
Пользователь получает понятное сообщение вместо пустой страницы».

---

## 16. Повторное использование фрагментов

Показать:

`podcast_card.html`

и подключение:

```django
{% include "podcasts_web/includes/podcast_card.html" %}
```

Также можно показать `episode_status.html`.

Сказать:

«Повторяющуюся разметку вынесли в отдельный шаблон.
Изменение карточки или статуса делается в одном месте».

---

## 17. Ссылки через {% url %}

Показать:

```django
{% url 'podcasts_web:detail' podcast.id %}
```

Сказать:

«Django ищет маршрут по имени.
`podcast.id` передаётся как параметр динамического URL».

---

## 18. Пространства имён

Показать:

`podcasts_web/urls.py`:

```python
app_name = "podcasts_web"
```

и:

```python
name="detail"
```

Сказать:

«Полное имя маршрута получается
`podcasts_web:detail`.
Namespace позволяет разным приложениям иметь одинаковые короткие
имена маршрутов без конфликтов».

---

## 19. Фильтры

Показать:

```django
{{ podcasts|length }}
```

и:

```django
{{ podcast.title|default:"Без названия" }}
```

Сказать:

«`length` возвращает количество элементов.
`default` задаёт значение для пустого или отсутствующего значения.
Фильтр изменяет представление данных, а не бизнес-логику».

---

## 20. Статические файлы

Показать начало `base.html`:

```django
{% load static %}
```

CSS:

```django
{% static 'homepage/css/style.css' %}
```

JS:

```django
{% static 'homepage/js/main.js' %}
```

Изображение:

```django
{% static 'homepage/img/logo.png' %}
```

Показать каталог:

`homepage/static/homepage/`.

Сказать:

«Django static строит корректный URL статического ресурса.
Путь к файлу не зашит вручную в HTML».

---

## 21. CSS

Открыть:

`homepage/static/homepage/css/style.css`.

Показать:

```css
.hero-section
.app-card
.metric-card
.error-page
```

Сказать:

«Это собственные стили проекта.
Если убрать подключение style.css, Bootstrap останется,
но собственное оформление исчезнет.

Проверить загрузку можно через DevTools → Network либо открыть
адрес static-файла».

---

## 22. JavaScript

Открыть:

`homepage/static/homepage/js/main.js`.

Показать:

```javascript
yearElement.textContent = new Date().getFullYear();
```

В браузере показать текущий год в footer.

Сказать:

«JavaScript автоматически устанавливает текущий год.
Проверить выполнение можно по footer и через DevTools → Network /
Console».

---

## 23. Разделение логики и отображения

Показать:

`podcasts_web/views.py` и `podcast_list.html`.

Сказать:

«Python выполняет загрузку, поиск, фильтрацию и подготовку context.
Шаблон отвечает за HTML, цикл, условия и визуальное представление.

Если меняется состав данных — меняю view или предметную логику.
Если меняется внешний вид — меняю HTML/CSS шаблон».

---

## 24. Отказ от HTML в Python

Показать поиск по проекту:

`page(`

В веб-представлениях вызовов быть не должно.

Показать:

```python
return render(...)
```

Сказать:

«В ПР5 HTML собирался Python-функцией `page()`.
В ПР6 HTML вынесен в Django Templates.
`render()`, context, `extends` и `include` уменьшают дублирование
и разделяют данные и отображение».

---

## 25. Целостность реализации

На примере `/podcasts/1/` пройти цепочку:

1. `podcast_planner/urls.py`
2. `podcasts_web/urls.py`
3. `podcasts_web/views.py`
4. `storage.py`
5. `data/podcasts.json`
6. context
7. `podcast_detail.html`
8. `base.html`
9. `navigation.html`
10. `style.css` и `main.js`
11. HTML в браузере

Сказать:

«Полный путь:
URL → маршрут приложения → view → загрузка JSON → Python-объект →
context → дочерний шаблон → base.html → static → HTTP-ответ →
браузер.

Если страница отображается неправильно, проверяю URLconf,
view, данные JSON, context, путь к template, шаблон и static-файлы».

---

## Короткое вступление

«В ПР6 я перевела веб-интерфейс Podcast Planner с формирования HTML
в Python на Django Templates. Предметная модель и JSON-хранилище
сохранены. Теперь используется архитектура
View → Context → Template → HTML».

## Логин для демонстрации

```text
admin
admin123
```
